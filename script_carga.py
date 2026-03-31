from faker import Faker
import random

disciplinas = [
    'Fundamentos de Programação', 
    'Programação Orientada a Objetos', 
    'Estruturas de Dados', 
    'Estrutura de Dados Avançada',
]

tipos_feedback = [
    'Elogio',
    'Crítica',
    'Sugestão',
]

feedbacks = []

faker = Faker('pt_BR')

# Integrar com o Pydantic quando o Willa fizer
for id in range(1000):
    feedbacks.append({
        'id': id,
        'disciplina': random.choice(disciplinas),
    })