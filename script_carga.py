from faker import Faker
import random

disciplinas = [
    'Fundamentos de Programação', 
    'Programação Orientada a Objetos', 
    'Estruturas de Dados', 
    'Estrutura de Dados Avançada',
]

monitores = [
    'Ana Amélia',
    'Iago Lô',
    'José Nilson',
    'Weryck Lemos',
    'João David',
    'Hanna Lavine',
    'Maria Vitória',
    'Matheus Mendes',
    'Cesário Filho',
    'Matheus Eugênio',
    'Emilson Filho',
    'Heitor Pimenta',
    'Pedro Edson',
    'Carla Cristina',
    'Luiz Guilherme',
    'Vicente de Paulo',
    'Jordan Pinheiro',
    'Carlos Nobre',
    'José Luis',
    'João Eudes',
    'Daniel Andrade',
    'João Filipe',
    'Antônio Pompeu',
    'Mário Martins',
    'João Eduardo'
]
# Será que valeria a pena relacionar disciplinas e monitores para constância na geração dos dados?

tipos_feedback = [
    'Elogio',
    'Crítica',
    'Sugestão',
]

def gerar_carga_inicial():
    feedbacks = []

    faker = Faker('pt_BR')

    # TODO: Integrar com o Pydantic quando o Willa fizer
    for id in range(1, 1001):
        feedbacks.append({
            'id': id,
            'disciplina': random.choice(disciplinas),
            'nome_monitor': random.choice(monitores),
            'tipo_mensagem': random.choice(tipos_feedback),
            'texto_feedback': faker.paragraph(),
            'data_submissao': faker.date_time_this_year().isoformat(),
            'hash_aluno': faker.sha256()
        })

    return feedbacks

if __name__ == "__main__":
    print("Iniciando a população do banco...")
    gerar_carga_inicial()
    