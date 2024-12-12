import pandas as pd
import numpy as np
from pymoo.core.problem import Problem  # Importação atualizada do pymoo
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import psycopg2
import time
import warnings
warnings.filterwarnings('ignore', category=UserWarning, message='pandas only supports SQLAlchemy')


def conectar_banco():
    conn = psycopg2.connect(
        host="db", #db se for pro docker, localhost se for local
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

    # Verificação dos dados carregados
    print(f"Numero de ativos: {len(df_ativos)}")
    print(f"Numero de manutencoes: {len(df_manutencoes)}")
    print("Exemplo de manutencoes:")
    print(df_manutencoes.head())

    return df_ativos, df_manutencoes

class ManutencaoProblem(Problem):
    def __init__(self, n_manutencoes, duracoes, custos, custos_falha):
        super().__init__(n_var=n_manutencoes, n_obj=1, n_ieq_constr=0, xl=0, xu=1)
        self.duracoes = duracoes
        self.custos = custos
        self.custos_falha = custos_falha

    def _evaluate(self, x, out, *args, **kwargs):
        x_bin = np.round(x)
        # Cálculo do custo total (custo de manutenção + custo de falha)
        custo_manutencao = x_bin * self.custos
        custo_falha = (1 - x_bin) * self.custos_falha
        f1 = np.sum(custo_manutencao + custo_falha, axis=1)
        out["F"] = f1.reshape(-1, 1)

def main():
    # Extração dos dados
    df_ativos, df_manutencoes = extrair_dados()

    # Pré-processamento dos dados
    manutencoes_pendentes = df_manutencoes.copy()
    n_manutencoes = len(manutencoes_pendentes)

    if n_manutencoes == 0:
        print("Nao ha manutencoes a serem otimizadas.")
        return

    duracoes = manutencoes_pendentes['duracao_horas'].astype(float).values
    custos = manutencoes_pendentes['custo'].astype(float).values
    # Definir custos de falha (por exemplo, 3 vezes o custo de manutenção)
    custos_falha = custos * 3

    # Configuração do problema de otimização
    problem = ManutencaoProblem(n_manutencoes, duracoes, custos, custos_falha)

    # Configuração do algoritmo NSGA-II
    algorithm = NSGA2(pop_size=50)

    # Execução da otimização
    res = minimize(problem,
                   algorithm,
                   ('n_gen', 50),
                   seed=1,
                   verbose=True)

    # Análise dos resultados
    melhores_indices = np.argmin(res.F)
    melhor_solucao = res.X[melhores_indices]

    # Exibição dos resultados
    print("Melhor solucao encontrada:")
    print("Manutencoes selecionadas:")
    manutencoes_selecionadas = []
    for i, val in enumerate(melhor_solucao):
        if val >= 0.5:
            manutencao = manutencoes_pendentes.iloc[i]
            manutencoes_selecionadas.append(manutencao)
            print(f"- Manutencao ID {manutencao['id']} no Ativo ID {manutencao['ativo_id']}")
    downtime_total = np.sum(np.round(melhor_solucao) * duracoes)
    print(f"Downtime total: {downtime_total} horas")

    if len(manutencoes_selecionadas) == 0:
        print("Nenhuma manutencao foi selecionada na melhor solucao.")

if __name__ == "__main__":
    main()
