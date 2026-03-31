from faker import Faker
import random

disciplinas = [
    'Fundamentos de Programação', 
    'Programação Orientada a Objetos', 
    'Estruturas de Dados', 
    'Estrutura de Dados Avançada',
]

# Mapeamento extraído da planilha com múltiplas alocações
alocacao_monitores = {
    'Ana Amélia': ['Fundamentos de Programação'],
    'Carlos': ['Fundamentos de Programação'],
    'José Nilson': ['Fundamentos de Programação'],
    'Matheus Mendes': ['Fundamentos de Programação'], # Assumindo que o primeiro Matheus é o Mendes
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
    'Matheus Eugênio': ['Fundamentos de Programação'], # Referenciado como Matheus Eg na imagem
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
# Será que valeria a pena relacionar disciplinas e monitores para constância na geração dos dados?

tipos_feedback = [
    'Elogio',
    'Crítica',
    'Sugestão',
]

def gerar_carga_inicial():
    feedbacks = []

    faker = Faker('pt_BR')

    nomes_monitores = list(alocacao_monitores.keys())

    # TODO: Integrar com o Pydantic quando o Willa fizer
    for id in range(1, 1001):
        monitor_escolhido = random.choice(nomes_monitores)
        disciplina_escolhida = random.choice(alocacao_monitores[monitor_escolhido])

        feedbacks.append({
            'id': id,
            'disciplina': disciplina_escolhida,
            'nome_monitor': monitor_escolhido,
            'tipo_mensagem': random.choice(tipos_feedback),
            'texto_feedback': faker.paragraph(),
            'data_submissao': faker.date_time_this_year().isoformat(),
            'hash_aluno': faker.sha256()
        })

    return feedbacks

if __name__ == "__main__":
    print("Iniciando a população do banco...")
    print(gerar_carga_inicial())