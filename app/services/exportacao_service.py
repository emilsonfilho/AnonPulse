import random
from datetime import datetime
import hashlib
import io
import zipfile

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

def mock_deltalake():
    """
    Função dublê que o Membro 3 (Você) vai usar para testar o streaming 
    enquanto o Membro 1 não termina o banco Delta Lake real.
    """
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

caminho_zip = ''

def gerar_csv_streaming():
    yield "id,disciplina,nome_monitor,tipo_mensagem,texto_feedback,data_submissao,hash_aluno\n"

    # TODO: Substituir a função mock_deltalake() pela consulta real ao Delta Lake quando estiver pronta.
    for registro in mock_deltalake():
        yield ",".join(str(valor) for valor in registro.values()) + "\n"

def gerar_zip_streaming():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        with zf.open('feedbacks.csv', 'w') as csvf:
          for linha in gerar_csv_streaming():
            csvf.write(linha.encode('utf-8'))

            chunk = buffer.getvalue()
            if chunk:
                yield chunk
                buffer.seek(0)
                buffer.truncate()
    yield buffer.getvalue()
              

# Se você rodar esse arquivo solto, ele imprime a lista no terminal pra você ver se deu bom:
if __name__ == "__main__":
    dados_teste = mock_deltalake()
    for linha in dados_teste:
        print(linha)