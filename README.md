# 🎓 AnonPulse (MongoDB & MinIO)

O **AnonPulse** é uma API Web desenvolvida com **FastAPI** para o gerenciamento de feedbacks anônimos no contexto acadêmico. Este repositório refere-se à entrega do Trabalho Prático 3 (TP3), que migra a persistência de dados para uma arquitetura NoSQL utilizando **MongoDB** (via ODM **Beanie**) e introduz o armazenamento de objetos em nuvem com o **MinIO**.

---

## 🚀 Tecnologias Utilizadas

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (100% Assíncrono)
* **Banco de Dados (NoSQL):** [MongoDB](https://www.mongodb.com/)
* **ODM (Object Document Mapper):** [Beanie](https://beanie-odm.dev/) (Integração nativa com Pydantic)
* **Object Storage:** [MinIO](https://min.io/) (via `aioboto3` para operações assíncronas)
* **Gerenciador de Dependências:** [uv](https://github.com/astral-sh/uv) (Rápido e determinístico)
* **Infraestrutura:** Docker & Docker Compose
* **Geração de Dados:** `Faker` (pt_BR)

---

## 📋 Atendimento aos Requisitos do TP3

Abaixo está o checklist de cumprimento das exigências do professor:

* [x] **Coleções e Relacionamentos:** Mais de 5 coleções. Uso de documentos embutidos (`Enrollment`, `MonitorAssignment`) e DBRefs (`Link`). Relações 1:N e N:M implementadas.
* [x] **CRUD Completo:** Operações implementadas em todas as entidades via arquitetura em camadas (`Routers` ➡️ `Services` ➡️ `Repositories`).
* [x] **Tratamento de Exceções:** Handlers globais e exceções customizadas implementados no diretório `app/core/exceptions`.
* [x] **Paginação:** Implementada em todas as listagens (`GET /`) utilizando `fastapi-pagination`.
* [x] **Upload de Arquivos (MinIO):** Entidade `Document` criada. Arquivos são salvos no bucket MinIO via streaming, e apenas os metadados residem no MongoDB.
* [x] **Dockerização:** Orquestração completa de 3 serviços (`api`, `mongo`, `minio`) conectados por uma rede interna no `compose.yml`.
* [x] **Script de Carga Realista:** Arquivo `seed.py` inserindo mais de 100 registros por entidade de forma coerente e relacional.
* [x] **Consultas Complexas (Aggregation Pipeline):** Consultas textuais (Case-insensitive), filtros de datas, contagens (`$group`) e cruzamento de coleções.

---

## 🏗️ Diagrama de Classes (Modelo de Documentos - Beanie)

```mermaid
classDiagram
    class Student {
        +PydanticObjectId id
        +str registration
        +List[BackLink] enrollments
    }
    class Enrollment {
        +PydanticObjectId id
        +datetime enrolled_at
        +Link[Student] student
        +Link[Classroom] classroom
    }
    class Classroom {
        +PydanticObjectId id
        +str cod
        +Link[Subject] subject
        +Link[Professor] professor
    }
    class Subject {
        +PydanticObjectId id
        +str cod
        +str name
    }
    class Professor {
        +PydanticObjectId id
        +str name
        +str email
    }
    class Monitor {
        +PydanticObjectId id
        +str registration
        +str name
        +str email
    }
    class MonitorAssignment {
        +PydanticObjectId id
        +int weekly_hours
        +Link[Monitor] monitor
        +Link[Classroom] classroom
    }
    class Feedback {
        +PydanticObjectId id
        +str text
        +int rating
        +MessageType type
        +Link[MonitorAssignment] assignment
    }
    class DocumentMetadata {
        +PydanticObjectId id
        +str original_filename
        +str content_type
        +Link[MonitorAssignment] assignment
    }

    Student "1" -- "*" Enrollment : possui
    Classroom "1" -- "*" Enrollment : matricula
    Classroom "1" -- "*" MonitorAssignment : aloca
    Monitor "1" -- "*" MonitorAssignment : executa
    MonitorAssignment "1" -- "*" Feedback : recebe
    MonitorAssignment "1" -- "*" DocumentMetadata : possui
    Classroom "*" -- "1" Subject : pertence
    Classroom "*" -- "1" Professor : ministrada_por

``` 

## ⚙️ Como Executar o Projeto via Docker (Recomendado)

O projeto foi configurado para subir com um único comando, garantindo que o FastAPI, MongoDB e MinIO comuniquem-se em uma rede fechada.

1. Configurar Variáveis de Ambiente
Renomeie o arquivo .env-example para .env.

```Bash
cp .env-example .env
```

(As credenciais do MongoDB e MinIO já estão pré-configuradas para o ambiente Docker).

1. Subir os Contêineres

```Bash
docker compose up --build
```

Serviços disponíveis:

🟢 API (Swagger): <http://localhost:8000/docs>

🟡 MongoDB: localhost:27017

🔴 MinIO Console (Web): <http://localhost:9001> (Acesso: minioadmin / minioadmin)

🗄️ Alternando entre MongoDB Local e Atlas (Nuvem)
Conforme requisito do trabalho, a troca de bancos é feita exclusivamente pelo arquivo .env. Basta comentar e descomentar as respectivas linhas:

```Bash
# MongoDB Local via Docker (ATUALMENTE ATIVO) ---

DATABASE_URL="mongodb://root:example@mongo:27017/anonpulse?authSource=admin"

# --- MongoDB Atlas na Nuvem (DESCOMENTE PARA ATIVAR) ---

# DATABASE_URL="mongodb+srv://<usuario>:<senha>@cluster0.mongodb.net/anonpulse?retryWrites=true&w=majority"
```

🌱 Povoando o Banco de Dados (Seed)
Foi criado um script robusto utilizando a biblioteca Faker para popular o banco de dados com mais de 100 registros realistas e consistentes por entidade.

Para executar a carga inicial, com o Docker rodando, abra um novo terminal e execute:

## Se tiver o UV instalado localmente

```Bash
uv run seed_mongo.py
```

## OU rodando o script por dentro do contêiner da API

```Bash
docker exec -it anonpulse python seed_mongo.py
```

## 📄 Organização da Equipe

A divisão detalhada das tarefas executadas por cada membro (Modelagem, Repositórios Beanie, Dockerização, MinIO, Script Faker, etc.) encontra-se no arquivo anexo divisao_tarefas.txt.
