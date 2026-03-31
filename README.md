# 🚀 AnonPulse

**Sistema de Gerenciamento e Exportação de Feedbacks de Monitoria**

O **AnonPulse** é uma plataforma desenvolvida para gerenciar feedbacks anônimos de alunos para monitores da UFC Quixadá. O projeto foca em alta performance e eficiência de recursos, utilizando uma arquitetura baseada em **Lakehouse (Delta Lake)** para persistência e **Streaming de Bytes** para exportação de dados, garantindo consumo mínimo de memória RAM no servidor.

Este projeto foi desenvolvido como requisito de avaliação para a disciplina de **Desenvolvimento de Software para Persistência**, ministrada pelo Prof. Regis Pires Magalhães.

---

## 🛠️ Tecnologias e Arquitetura

O sistema foi construído aplicando conceitos avançados de Persistência de Arquivos, Serialização e Manipulação de Fluxos de Memória (ByteStream):

* **[Python 3.12+]**: Linguagem base do projeto.
* **[FastAPI]**: Framework web assíncrono para roteamento e endpoints da API.
* **[Delta Lake / PyArrow]**: Motor de persistência de dados tabulares. Utiliza arquivos Parquet sob o capô com compressão **ZSTD** para otimizar operações analíticas e leitura incremental.
* **[Zipstream & IO]**: Bibliotecas utilizadas para compressão sem perda (*Lossless*) e geração de arquivos em tempo real via buffers de memória RAM, sem a necessidade de gravar arquivos temporários em disco.
* **[Hashlib]**: Geração de identificadores criptográficos seguros (SHA-256).

---

## ✨ Funcionalidades Principais (Requisitos)

* **CRUD de Feedbacks**: Operações completas de Criação, Leitura, Atualização e Exclusão integradas diretamente ao Delta Lake.
* **Exportação CSV via Streaming**: Endpoint que consulta o banco de dados e entrega milhares de registros de feedback linha a linha (`yield`) no formato `.csv`, evitando sobrecarga de memória (`Out of Memory`).
* **Exportação ZIP via Streaming**: Endpoint que aplica o algoritmo de compressão `ZIP_DEFLATED` em tempo real sobre os dados e entrega um pacote `.zip` puro ao cliente web usando `StreamingResponse`.
* **Geração de Hash**: Rota dedicada a transformar strings sensíveis (como a identificação oculta do aluno) em um Hash SHA-256 seguro.
* **Mock e Carga Inicial**: Script automatizado (`script_carga.py`) para geração de massa de dados simulando múltiplas alocações de monitores.

---

## ⚙️ Instalação e Execução

O projeto utiliza um gerenciamento de dependências moderno e rápido. Recomendamos o uso da ferramenta `uv` (ou o setup padrão via `pyproject.toml`).

### 1. Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/AnonPulse.git](https://github.com/seu-usuario/AnonPulse.git)
cd AnonPulse
```

### 2. Instalar as Dependências
```bash
uv venv
uv pip install -e .
```

### 3. Rodar a Carga Inicial dos Dados
```bash
python script_carpa.py
```

### 4. Iniciar o Servidor FastAPI
```bash
fastapi dev app/main.py
```

## 👥 Equipe e Divisão de Tarefas
A arquitetura do trabalho foi dividida de forma modular, garantindo que as camadas de Banco de Dados, API e Serviços funcionassem de forma independente:
1. Modelagem e implementação do banco de dados com Delta Lake (operações de Create, Insert, Update, Delete) e leitura incremental em lotes.
2. Configuração da arquitetura da API com FastAPI, criação das rotas HTTP, integração dos retornos via StreamingResponse e implementação do endpoint de criptografia/Hash (F7).
3. Implementação dos endpoints de streaming F5 e F6, script de carga via Faker e setup do pyproject.toml.

Made with 🤓☝️ by [Emilson Filho](https://github.com/emilsonfilho), [Willian Silva](https://github.com/WillianSilva51) and [Iago Lô](https://github.com/iagoolo)
