import pandas as pd
import numpy as np
import psycopg2
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings('ignore', category=UserWarning, message='pandas only supports SQLAlchemy')

def conectar_banco():
    """Conecta ao banco de dados PostgreSQL"""
    conn = psycopg2.connect(
        host="db",  # Use 'localhost' se estiver rodando localmente, db no Docker
        database="teste",
        user="postgres",
        password="postgres"
    )
    return conn


def puxar_melhores_manutencoes():
    """Extrai as melhores manutencoes com informacoes relevantes via JOIN"""
    conn = conectar_banco()

    query = """
    SELECT 
        mm.manutencao_id,
        mm.ativo_id,
        m.custo,
        m.duracao_horas,
        o.prioridade,
        a.nome AS nome_ativo,
        a.localizacao
    FROM melhores_manutencoes mm
    JOIN manutencoes m ON mm.manutencao_id = m.id
    JOIN ordens_servico o ON m.ordem_servico_id = o.id
    JOIN ativos a ON m.ativo_id = a.id;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def calcular_criticidade(df):
    """Adiciona a coluna de criticidade com base na prioridade"""
    mapa_prioridade = {"Alta": 3, "Media": 2, "Baixa": 1}
    df['criticidade'] = df['prioridade'].map(mapa_prioridade).fillna(1)
    return df


def aplicar_topsis(df):
    """Aplica o metodo TOPSIS para ordenar as manutencoes"""
    criterios = df[['criticidade', 'custo', 'duracao_horas']].values

    scaler = MinMaxScaler()
    criterios_normalizados = scaler.fit_transform(criterios)

    pesos = np.array([0.5, 0.3, 0.2])  # Criticidade tem maior peso
    beneficio = [1, -1, -1]

    criterios_ponderados = criterios_normalizados * pesos * beneficio

    ideal_positivo = criterios_ponderados.max(axis=0)
    ideal_negativo = criterios_ponderados.min(axis=0)

    dist_positivo = np.linalg.norm(criterios_ponderados - ideal_positivo, axis=1)
    dist_negativo = np.linalg.norm(criterios_ponderados - ideal_negativo, axis=1)

    df['indice_topsis'] = dist_negativo / (dist_positivo + dist_negativo)
    df['posicao_ordenada'] = df['indice_topsis'].rank(ascending=False).astype(int)

    return df.sort_values('posicao_ordenada')


def criar_tabela_manutencoes_ordenadas():
    """Cria a tabela de manutencoes ordenadas se nao existir"""
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS manutencoes_ordenadas (
            id SERIAL PRIMARY KEY,
            manutencao_id INTEGER REFERENCES manutencoes(id),
            ativo_id INTEGER REFERENCES ativos(id),
            criticidade INTEGER,
            custo NUMERIC,
            duracao_horas INTEGER,
            posicao_ordenada INTEGER
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()


def salvar_manutencoes_ordenadas(df):
    """Salva a lista ordenada no banco"""
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM manutencoes_ordenadas")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO manutencoes_ordenadas (manutencao_id, ativo_id, criticidade, custo, duracao_horas, posicao_ordenada)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            int(row['manutencao_id']),
            int(row['ativo_id']),
            int(row['criticidade']),
            float(row['custo']),
            int(row['duracao_horas']),
            int(row['posicao_ordenada'])
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Manutencoes ordenadas salvas com sucesso no banco de dados.")

def main():
    print("Extraindo melhores manutencoes...")
    df = puxar_melhores_manutencoes()

    if df.empty:
        print("Nenhuma manutencao encontrada para decisao multicriterio.")
        return

    print("Dados extraidos com sucesso. Calculando criticidade...")
    df = calcular_criticidade(df)

    print("Aplicando metodo TOPSIS para ordenacao...")
    df_ordenado = aplicar_topsis(df)

    # Configura display para mostrar todas as colunas e linhas no terminal
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')

    print("\n===== LISTA FINAL DE MANUTENCOES ORDENADAS =====")
    print(df_ordenado[['manutencao_id', 'ativo_id', 'criticidade', 'custo', 'duracao_horas', 'posicao_ordenada']].to_string(index=False))
    print("================================================")

    print("\nSalvando no banco...")
    criar_tabela_manutencoes_ordenadas()
    salvar_manutencoes_ordenadas(df_ordenado)

    print("Processo concluido com sucesso.")


if __name__ == "__main__":
    main()
