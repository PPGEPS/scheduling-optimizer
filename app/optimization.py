import pandas as pd
import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import psycopg2
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore', category=UserWarning, message='pandas only supports SQLAlchemy')


def conectar_banco():
    conn = psycopg2.connect(
        host="localhost",  # 'db' se estiver rodando no Docker, senao localhost
        database="teste",
        user="postgres",
        password="postgres"
    )
    return conn


def extrair_dados():
    conn = conectar_banco()
    df_ativos = pd.read_sql_query("SELECT * FROM ativos", conn)
    df_manutencoes = pd.read_sql_query("SELECT * FROM manutencoes", conn)
    conn.close()

    print(f"Numero de ativos: {len(df_ativos)}")
    print(f"Numero de manutencoes: {len(df_manutencoes)}")
    print("Exemplo de manutencoes:")
    print(df_manutencoes.head())

    return df_ativos, df_manutencoes

class ManutencaoProblem(Problem):
    def __init__(self, n_manutencoes, duracoes, custos, custos_falha):
        super().__init__(n_var=n_manutencoes, n_obj=2, n_ieq_constr=0, xl=0, xu=1)
        self.duracoes = duracoes
        self.custos = custos
        self.custos_falha = custos_falha

    def _evaluate(self, x, out, *args, **kwargs):
        x_bin = np.round(x)
        custo_total = np.sum(x_bin * self.custos + (1 - x_bin) * self.custos_falha, axis=1)
        downtime_total = np.sum(x_bin * self.duracoes, axis=1)
        out["F"] = np.column_stack([custo_total, downtime_total])

def escolher_melhor_solucao(res, peso_custo=0.5, peso_downtime=0.5):
    custos = res.F[:, 0]
    downtimes = res.F[:, 1]

    # Normalização
    custos_norm = (custos - np.min(custos)) / (np.max(custos) - np.min(custos) + 1e-9)
    downtimes_norm = (downtimes - np.min(downtimes)) / (np.max(downtimes) - np.min(downtimes) + 1e-9)

    # Cálculo do escore com pesos
    escores = peso_custo * custos_norm + peso_downtime * downtimes_norm
    melhor_idx = np.argmin(escores)  # Escolhe a solução com o menor escore
    return melhor_idx


def criar_tabela_melhores_manutencoes():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS melhores_manutencoes (
            id SERIAL PRIMARY KEY,
            manutencao_id INTEGER REFERENCES manutencoes(id),
            ativo_id INTEGER REFERENCES ativos(id)
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()


def salvar_melhores_manutencoes(manutencoes):
    conn = conectar_banco()
    cursor = conn.cursor()

    for manutencao in manutencoes:
        cursor.execute("""
            INSERT INTO melhores_manutencoes (manutencao_id, ativo_id)
            VALUES (%s, %s)
        """, (
            int(manutencao['id']),
            int(manutencao['ativo_id'])
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Melhores manutencoes salvas com sucesso no banco de dados.")


def main():
    df_ativos, df_manutencoes = extrair_dados()

    manutencoes_pendentes = df_manutencoes.copy()
    n_manutencoes = len(manutencoes_pendentes)

    if n_manutencoes == 0:
        print("Nao ha manutencoes para otimizar.")
        return

    duracoes = manutencoes_pendentes['duracao_horas'].astype(float).values
    custos = manutencoes_pendentes['custo'].astype(float).values
    custos_falha = custos * 3  # Penalidade por não realizar a manutenção

    problem = ManutencaoProblem(n_manutencoes, duracoes, custos, custos_falha)
    algorithm = NSGA2(pop_size=150)
    res = minimize(problem, algorithm, ('n_gen', 150), seed=1, verbose=False)

    melhores_indices = escolher_melhor_solucao(res, peso_custo=0.5, peso_downtime=0.5)
    melhor_solucao = res.X[melhores_indices]

    manutencoes_selecionadas = []
    print("\nManutencoes selecionadas:")
    for i, val in enumerate(melhor_solucao):
        if val >= 0.5:
            manutencao = manutencoes_pendentes.iloc[i]
            manutencoes_selecionadas.append(manutencao)
            print(f"- Manutencao ID {manutencao['id']} no Ativo ID {manutencao['ativo_id']}")

    downtime_total = np.sum(np.round(melhor_solucao) * duracoes)
    print(f"\nDowntime total: {downtime_total} horas")

    if len(manutencoes_selecionadas) > 0:
        criar_tabela_melhores_manutencoes()
        salvar_melhores_manutencoes(manutencoes_selecionadas)
    else:
        print("Nenhuma manutencao foi selecionada.")


if __name__ == "__main__":
    main()
