CREATE TABLE ativos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50),
    localizacao VARCHAR(100),
    data_aquisicao DATE,
    custo_aquisicao NUMERIC,
    vida_util INTEGER,
    custo_manutencao_anual NUMERIC
);

CREATE TABLE ordens_servico (
    id SERIAL PRIMARY KEY,
    ativo_id INTEGER REFERENCES ativos(id),
    descricao TEXT,
    prioridade VARCHAR(10),
    status VARCHAR(20),
    data_abertura DATE,
    data_conclusao DATE
);

CREATE TABLE manutencoes (
    id SERIAL PRIMARY KEY,
    ativo_id INTEGER REFERENCES ativos(id),
    ordem_servico_id INTEGER REFERENCES ordens_servico(id),
    tipo_manutencao VARCHAR(20),
    custo NUMERIC,
    data_manutencao DATE,
    duracao_horas INTEGER
);

CREATE TABLE recursos (
    id SERIAL PRIMARY KEY,
    manutencao_id INTEGER REFERENCES manutencoes(id),
    nome VARCHAR(100),
    quantidade INTEGER,
    custo_unitario NUMERIC
);

CREATE TABLE historico_utilizacao (
    id SERIAL PRIMARY KEY,
    ativo_id INTEGER REFERENCES ativos(id),
    data DATE,
    horas_utilizadas INTEGER
);

