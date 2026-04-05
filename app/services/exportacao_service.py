from app.database.delta_manager import FeedbackRepository
import zipstream
import zipfile
import csv
import io

# Mapeamento extraído da planilha com múltiplas alocações
alocacao_monitores = {
    "Ana Amélia": ["Fundamentos de Programação"],
    "Carlos": ["Fundamentos de Programação"],
    "José Nilson": ["Fundamentos de Programação"],
    "Matheus Mendes": ["Fundamentos de Programação"],
    "Weryck Lemos": ["Fundamentos de Programação", "Estruturas de Dados"],
    "João Filipe": ["Fundamentos de Programação"],
    "Vicente": ["Fundamentos de Programação"],
    "Alana": ["Fundamentos de Programação"],
    "Daniel": ["Fundamentos de Programação"],
    "Jordan": ["Fundamentos de Programação"],
    "Maria Vitória": ["Fundamentos de Programação"],
    "Pompeu": ["Fundamentos de Programação"],
    "Iago Lô": ["Fundamentos de Programação"],
    "Denilso": ["Fundamentos de Programação"],
    "Pedro Edson": ["Fundamentos de Programação", "Estruturas de Dados"],
    "Matheus Eugênio": ["Fundamentos de Programação"],
    "Hanna Lavine": ["Fundamentos de Programação"],
    "Luiz Guilherme": ["Fundamentos de Programação"],
    "Brandão": ["Fundamentos de Programação"],
    "Eudes": ["Fundamentos de Programação"],
    "Cesário Filho": ["Fundamentos de Programação"],
    "Carla Cristina": ["Programação Orientada a Objetos"],
    "Emilson Filho": ["Estruturas de Dados", "Estrutura de Dados Avançada"],
    "Mario": ["Estruturas de Dados"],
    "Heitor Pimenta": ["Estrutura de Dados Avançada"],
}

tipos_feedback = ["Elogio", "Crítica", "Sugestão"]

campos = [
    "id",
    "disciplina",
    "nome_monitor",
    "tipo_mensagem",
    "texto_feedback",
    "data_submissao",
    "hash_aluno",
]


def gerar_linha_csv(registro):
    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer, fieldnames=campos, quoting=csv.QUOTE_MINIMAL, lineterminator="\n"
    )
    writer.writerow(registro)
    return buffer.getvalue()


def gerar_csv_streaming():
    repo = FeedbackRepository(table_path="data/feedbacks_delta")
    yield ",".join(campos) + "\n"

    for lote in repo.read():
        for registro in lote:
            yield gerar_linha_csv(registro)


def gerar_bytes_csv():
    for linha in gerar_csv_streaming():
        yield linha.encode("utf-8")


def gerar_zip_streaming():
    zf = zipstream.ZipFile(mode="w", compression=zipfile.ZIP_DEFLATED)
    zf.write_iter("feedbacks.csv", gerar_bytes_csv())

    return zf


if __name__ == "__main__":
    print("--- Testando o Streaming de CSV ---")
    for linha in gerar_csv_streaming():
        print(linha, end="")

    print("\n--- Testando o Streaming de ZIP ---")
    pacote = b""
    for chunk in gerar_zip_streaming():
        pacote += chunk
        print(f"Recebendo chunk de bytes: {len(chunk)} bytes")

    nome_arquivo = "feedbacks_teste.zip"
    with open(nome_arquivo, "wb") as f:
        f.write(pacote)

    print("\n--- Verificando integridade do arquivo ZIP ---")
