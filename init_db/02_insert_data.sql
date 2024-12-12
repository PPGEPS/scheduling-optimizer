-- Inserção de dados na tabela 'ativos'
INSERT INTO ativos (nome, tipo, localizacao, data_aquisicao, custo_aquisicao, vida_util, custo_manutencao_anual) VALUES
('Compressor A', 'Compressor', 'Setor 1', '2015-06-15', 50000, 10, 5000),
('Bomba B', 'Bomba', 'Setor 2', '2016-08-20', 30000, 8, 3000),
('Turbina C', 'Turbina', 'Setor 3', '2017-09-10', 75000, 12, 7500),
('Gerador D', 'Gerador', 'Setor 4', '2018-03-05', 60000, 15, 6000),
('Motor E', 'Motor', 'Setor 5', '2019-11-22', 45000, 9, 4500),
('Caldeira F', 'Caldeira', 'Setor 6', '2020-01-17', 80000, 20, 8000),
('Ventilador G', 'Ventilador', 'Setor 7', '2021-05-30', 25000, 7, 2500),
('Transformador H', 'Transformador', 'Setor 8', '2014-12-12', 90000, 25, 9000),
('Esteira I', 'Esteira', 'Setor 9', '2013-07-08', 35000, 10, 3500),
('Robô J', 'Robô', 'Setor 10', '2022-02-14', 120000, 15, 12000);

-- Inserção de dados na tabela 'ordens_servico'
INSERT INTO ordens_servico (ativo_id, descricao, prioridade, status, data_abertura, data_conclusao) VALUES
(1, 'Reparo no compressor devido a ruído excessivo', 'Alta', 'Concluída', '2022-01-10', '2022-01-12'),
(2, 'Substituição de válvula desgastada', 'Média', 'Concluída', '2022-02-15', '2022-02-16'),
(3, 'Manutenção preventiva na turbina', 'Baixa', 'Concluída', '2022-03-20', '2022-03-21'),
(4, 'Falha elétrica no gerador', 'Alta', 'Concluída', '2022-04-05', '2022-04-07'),
(5, 'Lubrificação do motor', 'Média', 'Concluída', '2022-05-18', '2022-05-18'),
(6, 'Inspeção de segurança na caldeira', 'Alta', 'Concluída', '2022-06-25', '2022-06-26'),
(7, 'Troca de rolamentos do ventilador', 'Média', 'Concluída', '2022-07-30', '2022-07-31'),
(8, 'Atualização de software do transformador', 'Baixa', 'Concluída', '2022-08-15', '2022-08-15'),
(9, 'Ajuste de velocidade da esteira', 'Média', 'Concluída', '2022-09-10', '2022-09-11'),
(10, 'Calibração do robô', 'Alta', 'Concluída', '2022-10-05', '2022-10-06'),
(1, 'Substituição de filtro do compressor', 'Baixa', 'Concluída', '2022-11-12', '2022-11-12'),
(2, 'Verificação de vazamento na bomba', 'Média', 'Concluída', '2022-12-01', '2022-12-02'),
(3, 'Reparo em pás da turbina', 'Alta', 'Aberta', '2023-01-15', NULL),
(4, 'Manutenção preventiva no gerador', 'Baixa', 'Aberta', '2023-02-20', NULL),
(5, 'Substituição de correias do motor', 'Média', 'Em andamento', '2023-03-10', NULL),
(6, 'Limpeza interna da caldeira', 'Baixa', 'Aberta', '2023-04-05', NULL),
(7, 'Verificação elétrica do ventilador', 'Média', 'Aberta', '2023-04-12', NULL),
(8, 'Reparo de sobrecarga no transformador', 'Alta', 'Aberta', '2023-04-20', NULL),
(9, 'Alinhamento da esteira', 'Média', 'Aberta', '2023-04-25', NULL),
(10, 'Atualização de firmware do robô', 'Alta', 'Aberta', '2023-05-01', NULL);

-- Inserção de dados na tabela 'manutencoes'
INSERT INTO manutencoes (ativo_id, ordem_servico_id, tipo_manutencao, custo, data_manutencao, duracao_horas) VALUES
(1, 1, 'Corretiva', 2000, '2022-01-12', 5),
(2, 2, 'Corretiva', 1500, '2022-02-16', 4),
(3, 3, 'Preventiva', 1000, '2022-03-21', 3),
(4, 4, 'Corretiva', 2500, '2022-04-07', 6),
(5, 5, 'Preventiva', 800, '2022-05-18', 2),
(6, 6, 'Inspeção', 1200, '2022-06-26', 4),
(7, 7, 'Corretiva', 900, '2022-07-31', 3),
(8, 8, 'Atualização', 500, '2022-08-15', 1),
(9, 9, 'Ajuste', 700, '2022-09-11', 2),
(10, 10, 'Calibração', 1800, '2022-10-06', 5),
(1, 11, 'Preventiva', 600, '2022-11-12', 2),
(2, 12, 'Inspeção', 750, '2022-12-02', 3);

-- Inserção de dados na tabela 'recursos'
INSERT INTO recursos (manutencao_id, nome, quantidade, custo_unitario) VALUES
(1, 'Filtro de ar', 2, 100),
(1, 'Mão de obra', 5, 50),
(2, 'Válvula', 1, 500),
(2, 'Mão de obra', 4, 50),
(3, 'Lubrificante', 3, 80),
(3, 'Mão de obra', 3, 50),
(4, 'Componente elétrico', 2, 600),
(4, 'Mão de obra', 6, 50),
(5, 'Óleo lubrificante', 2, 70),
(5, 'Mão de obra', 2, 50),
(6, 'Equipamento de inspeção', 1, 500),
(6, 'Mão de obra', 4, 50),
(7, 'Rolamento', 4, 150),
(7, 'Mão de obra', 3, 50),
(8, 'Software de atualização', 1, 300),
(8, 'Mão de obra', 1, 50),
(9, 'Ferramenta de ajuste', 1, 200),
(9, 'Mão de obra', 2, 50),
(10, 'Equipamento de calibração', 1, 1000),
(10, 'Mão de obra', 5, 50),
(11, 'Filtro', 1, 100),
(11, 'Mão de obra', 2, 50),
(12, 'Equipamento de detecção', 1, 400),
(12, 'Mão de obra', 3, 50);

-- Inserção de dados na tabela 'historico_utilizacao'
-- Dados mensais para cada ativo ao longo de um ano
INSERT INTO historico_utilizacao (ativo_id, data, horas_utilizadas) VALUES
-- Ativo 1
(1, '2022-01-31', 160),
(1, '2022-02-28', 150),
(1, '2022-03-31', 170),
(1, '2022-04-30', 165),
(1, '2022-05-31', 160),
(1, '2022-06-30', 170),
(1, '2022-07-31', 155),
(1, '2022-08-31', 160),
(1, '2022-09-30', 165),
(1, '2022-10-31', 170),
(1, '2022-11-30', 160),
(1, '2022-12-31', 150),
-- Ativo 2
(2, '2022-01-31', 140),
(2, '2022-02-28', 130),
(2, '2022-03-31', 160),
(2, '2022-04-30', 150),
(2, '2022-05-31', 155),
(2, '2022-06-30', 145),
(2, '2022-07-31', 150),
(2, '2022-08-31', 160),
(2, '2022-09-30', 155),
(2, '2022-10-31', 150),
(2, '2022-11-30', 145),
(2, '2022-12-31', 140),
-- Ativo 3
(3, '2022-01-31', 180),
(3, '2022-02-28', 175),
(3, '2022-03-31', 185),
(3, '2022-04-30', 190),
(3, '2022-05-31', 195),
(3, '2022-06-30', 185),
(3, '2022-07-31', 180),
(3, '2022-08-31', 190),
(3, '2022-09-30', 185),
(3, '2022-10-31', 180),
(3, '2022-11-30', 175),
(3, '2022-12-31', 170),
-- Repita para os demais ativos
-- Ativo 4
(4, '2022-01-31', 200),
(4, '2022-02-28', 190),
(4, '2022-03-31', 195),
-- ... continue até dezembro
-- Ativo 5
(5, '2022-01-31', 120),
(5, '2022-02-28', 110),
(5, '2022-03-31', 130),
-- ... continue até dezembro
-- Ativo 6
(6, '2022-01-31', 100),
(6, '2022-02-28', 105),
(6, '2022-03-31', 95),
-- ... continue até dezembro
-- Ativo 7
(7, '2022-01-31', 160),
(7, '2022-02-28', 165),
(7, '2022-03-31', 170),
-- ... continue até dezembro
-- Ativo 8
(8, '2022-01-31', 150),
(8, '2022-02-28', 155),
(8, '2022-03-31', 160),
-- ... continue até dezembro
-- Ativo 9
(9, '2022-01-31', 130),
(9, '2022-02-28', 135),
(9, '2022-03-31', 140),
-- ... continue até dezembro
-- Ativo 10
(10, '2022-01-31', 210),
(10, '2022-02-28', 220),
(10, '2022-03-31', 230);
-- ... continue até dezembro

-- Inserção de dados adicionais nas tabelas 'ordens_servico' e 'manutencoes' para os ativos restantes
-- Ordens de serviço para ativos 4 a 10
INSERT INTO ordens_servico (ativo_id, descricao, prioridade, status, data_abertura, data_conclusao) VALUES
(4, 'Revisão geral do gerador', 'Alta', 'Concluída', '2022-06-15', '2022-06-17'),
(5, 'Troca de correias do motor', 'Média', 'Concluída', '2022-07-10', '2022-07-11'),
(6, 'Teste de pressão na caldeira', 'Alta', 'Concluída', '2022-08-05', '2022-08-06'),
(7, 'Limpeza das pás do ventilador', 'Baixa', 'Concluída', '2022-09-12', '2022-09-12'),
(8, 'Substituição de isoladores do transformador', 'Média', 'Concluída', '2022-10-20', '2022-10-21'),
(9, 'Lubrificação da esteira', 'Baixa', 'Concluída', '2022-11-25', '2022-11-25'),
(10, 'Verificação dos sensores do robô', 'Alta', 'Concluída', '2022-12-05', '2022-12-06');

-- Manutenções correspondentes
INSERT INTO manutencoes (ativo_id, ordem_servico_id, tipo_manutencao, custo, data_manutencao, duracao_horas) VALUES
(4, 13, 'Preventiva', 3000, '2022-06-17', 8),
(5, 14, 'Corretiva', 1200, '2022-07-11', 3),
(6, 15, 'Inspeção', 1800, '2022-08-06', 5),
(7, 16, 'Limpeza', 600, '2022-09-12', 2),
(8, 17, 'Corretiva', 2200, '2022-10-21', 6),
(9, 18, 'Preventiva', 800, '2022-11-25', 2),
(10, 19, 'Inspeção', 2000, '2022-12-06', 5);

-- Recursos correspondentes
INSERT INTO recursos (manutencao_id, nome, quantidade, custo_unitario) VALUES
(13, 'Mão de obra', 8, 50),
(13, 'Peças de reposição', 5, 200),
(14, 'Correias', 2, 150),
(14, 'Mão de obra', 3, 50),
(15, 'Equipamento de teste', 1, 800),
(15, 'Mão de obra', 5, 50),
(16, 'Material de limpeza', 1, 100),
(16, 'Mão de obra', 2, 50),
(17, 'Isoladores', 4, 400),
(17, 'Mão de obra', 6, 50),
(18, 'Lubrificante', 2, 80),
(18, 'Mão de obra', 2, 50),
(19, 'Equipamento de inspeção', 1, 1000),
(19, 'Mão de obra', 5, 50);

-- Atualização de status de ordens de serviço abertas para simular progresso
UPDATE ordens_servico SET status = 'Em andamento', data_conclusao = '2023-05-15' WHERE id = 13;
UPDATE ordens_servico SET status = 'Concluída', data_conclusao = '2023-05-20' WHERE id = 14;
