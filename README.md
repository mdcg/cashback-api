# cashback-api

## Considerações Iniciais

Gostaria de agradecer primeiramente a oportunidade de estar participando do processo seletivo. Foi um desafio bem interessante, pude mostrar bastante do meu *know-how* e acredito ter chegado em uma implementação muito boa. Espero que gostem. :)

Dada a natureza do problema proposto, e a partir de algumas análises realizadas, utilizei para a solução deste problema [Arquitetura Hexagonal](https://www.youtube.com/watch?v=X_EPcBNI5xU). O domínio da nossa aplicação ficou totalmente isolado e totalmente agnóstico à tecnologias.

A API que foi referenciada no teste prosposto não estava funcionando. Deste modo, tomei a liberdade para criar dois servidores Mock: Uma **API** que retorna o acumulado de cashback e um **Worker** que irá processar as vendas dos revendedores (a lógica de ambos será explicada mais abaixo).

Para facilitar os testes locais, todos os sistemas podem ser executados com o **Docker** e **Docker Compose**. Desta maneira, se for pertinente testar utilizando estas tecnologias, certifique-se de tê-las instaladas em sua máquina.

*Documentação do Docker e Docker Compose:*
* [Get Started with Docker](https://www.docker.com/get-started)
* [Overview of Docker Compose](https://docs.docker.com/compose/)

*Guia de instalação do Docker e Docker Compose (Ubuntu):*
* [Install Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* [Install Docker Compose](https://docs.docker.com/compose/install/)

Para facilitar a execução de todo sistema, sugiro que siga as instruções da seção *"Executando o sistema localmente"*, pois lá será apresentado alguns comandos no `Makefile` que são bastante pertinentes.

### Tecnologias

Mesmo com o fato de ter sido utilizada Arquitetura Hexagonal para resolução deste problema, ainda assim é pertinente falarmos sobre as principais implementações deste sistema.

* Como linguagem de programação, foi utilizado o Python na versão 3.10+;
* Existem dois adaptadores de bancos de dados: Um "Em memória" e outro utilizando o PostgreSQL na versão 11+;
* Foi implementado um adaptador para publicar mensagens em filas do RabbitMQ 3.10.7;
* Foi implementado um adaptador de autenticação que utiliza o JWT;
* Foi implementado um adaptador para enviar requisições HTTP para APIs externas;
* O sistema é servido a partir de uma interface RESTful que foi construída utilizando o framework Flask;
* Existem dois servidores Mock: Um para consultar o acumulado de cashback de um determinado revendedor (também com Flask) e outro para processar os status das vendas de maneira assíncrona (utilizando o framework Pika);
* Como dito anteriormente, também foram utilizados o Docker e o Docker Compose para facilitar a execução de todos os sistemas em conjunto.


## Diagramas do Sistemas

Para facilitar a visualização e comunicação do sistema com os servidores Mock, abaixo segue alguns diagramas bastante pertinentes:

<Colocar imagens dos diagramas>

## Executando o sistema localmente

Novamente, é reforçada a utilização do **Docker** e do **Docker Compose** para a execução dos sistemas. Abaixo seguem os comandos que deverão ser executados em sequência para que tudo funcione corretamente.

Inicializando as dependências (PostgreSQL, Provisionamento do Banco de Dados e RabbitMQ):

```bash
make start-deps
```

Inicializando os servidores Mock (API RESTful e Worker)

```bash
make start-mock-servers
```

Inicializando a API RESTful do problema proposto:

```bash
make start-api
```

As dependências e os servidores Mock são executados em background. Se achar pertinente e desejar visualizar os logs dos mesmos, basta seguir o seguinte passo-a-passo:

```bash
# Busque pelo identificador do container que deseja visualizar os logs
# (que está na coluna "CONTAINER ID")
docker container ls

# Insira o identificador no seguinte comando:
docker logs <identificador_do_container> -f

# Caso você não queira ficar "acompanhando os logs", remova a opção -f
```

## Executando os testes

Para executar os testes unitários, é interessante que você crie uma **virtualenv** antes. Abaixo temos o passo-a-passo para criar, inicializar e instalar as bibliotecas necessárias para o funcionamento dos testes:

```
python -m venv env
source env/bin/activate
make install
```

Para executar os testes, execute:

```
make tests
```

Caso você queira checar se há alguma vulnerabilidade:

```
make security
```

Também temos um linter para assegurar que as boas práticas no desenvolvimento com a linguagem Python estão sendo seguidas:

```
make lint
```

## Conclusão

Novamente, agradeço a oportunidade e espero ter entregado algo digno do que era esperado para este desafio. Qualquer dúvida ou questionamento, fiquem a vontade para me contactarem. Valeu, pessoal!
