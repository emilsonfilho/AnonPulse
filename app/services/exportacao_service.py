import random
from datetime import datetime
import hashlib
import zipstream
import zipfile
import csv
import io

# Mapeamento extraído da planilha com múltiplas alocações
alocacao_monitores = {
    'Ana Amélia': ['Fundamentos de Programação'],
    'Carlos': ['Fundamentos de Programação'],
    'José Nilson': ['Fundamentos de Programação'],
    'Matheus Mendes': ['Fundamentos de Programação'],
    'Weryck Lemos': ['Fundamentos de Programação', 'Estruturas de Dados'],
    'João Filipe': ['Fundamentos de Programação'],
    'Vicente': ['Fundamentos de Programação'],
    'Alana': ['Fundamentos de Programação'],
    'Daniel': ['Fundamentos de Programação'],
    'Jordan': ['Fundamentos de Programação'],
    'Maria Vitória': ['Fundamentos de Programação'],
    'Pompeu': ['Fundamentos de Programação'],
    'Iago Lô': ['Fundamentos de Programação'],
    'Denilso': ['Fundamentos de Programação'],
    'Pedro Edson': ['Fundamentos de Programação', 'Estruturas de Dados'],
    'Matheus Eugênio': ['Fundamentos de Programação'],
    'Hanna Lavine': ['Fundamentos de Programação'],
    'Luiz Guilherme': ['Fundamentos de Programação'],
    'Brandão': ['Fundamentos de Programação'],
    'Eudes': ['Fundamentos de Programação'],
    'Cesário Filho': ['Fundamentos de Programação'],
    'Carla Cristina': ['Programação Orientada a Objetos'],
    'Emilson Filho': ['Estruturas de Dados', 'Estrutura de Dados Avançada'],
    'Mario': ['Estruturas de Dados'],
    'Heitor Pimenta': ['Estrutura de Dados Avançada']
}

tipos_feedback = ['Elogio', 'Crítica', 'Sugestão']

campos = ['id', 'disciplina', 'nome_monitor', 'tipo_mensagem', 'texto_feedback', 'data_submissao', 'hash_aluno']

def mock_deltalake():
    feedbacks_mock = []
    nomes_monitores = list(alocacao_monitores.keys())
    
    for id_falso in range(1, 11): # Gerando só 10 registros para teste rápido
        monitor_sorteado = random.choice(nomes_monitores)
        disciplina_correta = random.choice(alocacao_monitores[monitor_sorteado])
        
        # Criando um hash fake rapidinho usando a biblioteca nativa hashlib
        hash_fake = hashlib.sha256(f"aluno_anonimo_{id_falso}".encode()).hexdigest()

        feedbacks_mock.append({
            'id': id_falso,
            'disciplina': disciplina_correta,
            'nome_monitor': monitor_sorteado,
            'tipo_mensagem': random.choice(tipos_feedback),
            'texto_feedback': f"Texto de teste simulando a mensagem do feedback {id_falso}.",
            'data_submissao': datetime.now().isoformat(),
            'hash_aluno': hash_fake
        })
        
    return feedbacks_mock

def gerar_linha_csv(registro):
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=campos, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(registro)
    return buffer.getvalue()

def gerar_csv_streaming():
    # TODO: Substituir a função mock_deltalake() pela consulta real ao Delta Lake quando estiver pronta.
    yield ",".join(campos) + "\n"

    for registro in mock_deltalake():
        yield gerar_linha_csv(registro)

def gerar_bytes_csv():
    for linha in gerar_csv_streaming():
        yield linha.encode('utf-8')

def gerar_zip_streaming():
    zf =  zipstream.ZipFile(mode='w', compression=zipfile.ZIP_DEFLATED)
    zf.write_iter('feedbacks.csv', gerar_bytes_csv())
    
    return zf

if __name__ == "__main__":
    print("--- Testando o Streaming de CSV ---")
    for linha in gerar_csv_streaming():
        print(linha, end='')
    
    print("\n--- Testando o Streaming de ZIP ---")
    pacote = b''
    for chunk in gerar_zip_streaming():
        pacote += chunk
        print(f"Recebendo chunk de bytes: { len(chunk) } bytes")

    nome_arquivo = 'feedbacks_teste.zip'
    with open(nome_arquivo, 'wb') as f:
        f.write(pacote)

    print("\n--- Verificando integridade do arquivo ZIP ---")
    