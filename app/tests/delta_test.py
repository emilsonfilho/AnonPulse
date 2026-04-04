import os
import shutil # Biblioteca para apagar pastas
from app.database.delta_manager import FeedbackRepository

# 1. Configuração do ambiente de teste
pasta_banco = "./app/tests/data_delta_test"

# Limpa o teste anterior se existir (opcional)
if os.path.exists(pasta_banco):
    shutil.rmtree(pasta_banco)

repo = FeedbackRepository(pasta_banco)

# 2. Testando o INSERT
print("Inserindo dados de teste...")
dados_exemplo = {
    "disciplina": "Persistência",
    "nome_monitor": "Iago",
    "tipo_mensagem": "Elogio",
    "texto_feedback": "A persistência está funcionando!",
    "data_submissao": "2026-04-03",
    "hash_aluno": "hash123"
}

id_gerado = repo.insert(dados_exemplo)
print(f"Feedback inserido com ID: {id_gerado}")

# 3. Testando o READ
print("\nLendo dados do Delta Lake:")
for batch in repo.read(batch_size=1):
    for registro in batch:
        print(f"Registro encontrado: {registro}")

# 4. Testando o VACUUM
print("\nRodando faxina (Vacuum)...")
repo.vacuum()
print("Teste finalizado!")