Este projeto realiza a otimização e priorização de manutenções de ativos industriais com o objetivo de automatizar a criação de agendas dos funcionarios. Utilizando containers no Docker, cria um banco de dados generico com uma serie de manutenções a serem feitas. Ele utiliza um algoritmo de otimização multiobjetivo para selecionar as melhores manutenções, minimizando custos e tempo de inatividade (downtime). Após a otimização, um algoritmo de decisão multicritério (TOPSIS) reordena as manutenções de acordo com sua criticidade. Temos como objetivo futuro enviar para a IA treinado pelo Gustavo para montar a agenda dos funcionarios automaticamente.

***Tecnologias Utilizadas:***

Python: Linguagem principal para desenvolvimento.

PostgreSQL: Banco de dados relacional para armazenar informações sobre ativos e manutenções.

pymoo: Biblioteca para otimização multiobjetivo (NSGA-II).

pandas: Manipulação e análise de dados.

psycopg2: Conexão com PostgreSQL.

scikit-learn: Implementação do algoritmo TOPSIS.

Docker: Para conteinerização e execução do sistema.

***Como executar o projeto:***

1 - Certifique-se de ter o Docker instalado em seu computador <br>
      Caso nao tenha, acesse https://docs.docker.com/ para fazer o download <br><br>

2 - Após baixar os arquivos do projeto, crie uma pasta e deixe-os na mesma hierarquia como mostra o repositorio <br><br>

3 - Abra o terminal, vá até a pasta e rode os seguintes comandos: <br>
docker-compose build (para a construção dos containers) <br>
docker-compose up (para rodar os algoritmos) <br>
docker-compose down (para parar de rodar os algoritmos) <br>


***Funcionamento do projeto:***
otimization.py: <br>
Extrai os dados das manutenções do banco de dados <br>
Utiliza o NSGA-II para otimizar as manutenções levando em conta: custo, duração e impacto de falha <br>
Salva lista otimizada <br><br>


decision.py: <br>
Extrai os dados das manutenções otimizadas do banco de dados <br>
Aplica o método TOPSIS para definir a prioridade de execução de acordo com: criticidade, custo e duração <br>
Salva a lista otimizada e re-ordenada no banco de dados. <br><br>

run.py: <br>
É o código responsavel por rodar o otimization e o decision corretamente <br>
Serve apenas para chamar os outros dois na ordem correta.
