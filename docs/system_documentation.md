# Visão Geral

- O AnonPulse é uma API web assíncrona voltada ao gerenciamento de feedbacks anônimos em contextos acadêmicos;
- O sistema permite cadastrar professores, disciplinas, turmas, alunos, matrículas, monitores, atribuições de monitoria e feedbacks;
- O fluxo principal é receber feedbacks de estudantes de forma anônima, associá-los a uma turma e a um monitor, e armazenar os dados de forma consistente no MongoDB;
- Também há suporte a upload de arquivos e metadados de documentos, que são armazenados no MinIO.

## Arquitetura do Sistema

- A aplicação segue uma estrutura em camadas:
  - `app/api`: definição das rotas e endpoints da API;
  - `app/services`: regras de negócio e orquestração dos fluxos principais;
  - `app/repositories`: acesso e persistência dos documentos no banco;
  - `app/models`: modelos de documentos do Beanie;
  - `app/schemas`: validação e serialização dos dados;
  - `app/core`: configurações, inicialização do banco, enums e exceções compartilhadas.
- O banco utilizado é o MongoDB, com o ODM Beanie para integração com models Pydantic;
- O armazenamento de arquivos é feito no MinIO, enquanto os metadados ficam persistidos no MongoDB.

## Entidades Principais

- `Subject`: representa uma disciplina acadêmica;
- `Professor`: representa o responsável por uma disciplina ou turma;
- `Classroom`: representa uma turma vinculada a uma disciplina e a um professor;
- `Student`: representa o estudante, com identificação anonimizada via hash;
- `Enrollment`: representa a matrícula do estudante em uma turma;
- `Monitor`: representa o monitor responsável por acompanhar uma turma;
- `MonitorAssignment`: representa a atribuição de um monitor a uma turma;
- `Feedback`: representa o feedback enviado por um aluno para um monitor em uma turma;
- `DocumentMetadata`: representa os metadados de um documento enviado para o MinIO.

## Fluxos Principais

- Cadastro de entidades acadêmicas: professores, disciplinas e turmas;
- Criação de matrículas e vínculo entre estudante e turma;
- Cadastro de monitores e atribuição de monitores a turmas;
- Submissão de feedbacks com anonimização do identificador do estudante;
- Upload e consulta de documentos relacionados a uma atribuição de monitoria;
- Geração de dados iniciais por meio de scripts de carga.

## Regras de Negócio e Operação

- O identificador real do aluno nunca deve ser salvo em texto puro;
- Cada feedback deve ser associado a uma turma e a um monitor válidos;
- A API deve oferecer paginação nas listagens;
- As exceções devem ser tratadas centralmente para retornar respostas consistentes;
- O sistema deve ser executável via Docker para facilitar o ambiente de desenvolvimento e testes.

## Execução do Sistema

- O ambiente pode ser iniciado com Docker Compose;
- O projeto conta com um serviço para a API, outro para o MongoDB e outro para o MinIO;
- O seed de dados pode ser executado para popular o banco com dados coerentes e realistas.

## Observações de Manutenção

- A documentação de regras específicas fica concentrada em `docs/business_rules.md`;
- A documentação técnica e funcional deste sistema deve ser mantida atualizada sempre que houver mudança de fluxo, modelo ou regra de negócio.
