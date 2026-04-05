import os
import shutil
from datetime import datetime

from app.database.delta_manager import FeedbackRepository

# 1. Configuração do ambiente de teste
pasta_banco = "./app/tests/data_delta_test"

# Limpa o teste anterior se existir (para garantir que o count seja sempre 1 no teste)
if os.path.exists(pasta_banco):
    shutil.rmtree(pasta_banco)

repo = FeedbackRepository(pasta_banco)

# 2. Testando o INSERT
print("--- Testando INSERT ---")
dados_exemplo = {
    "disciplina": "Persistência",
    "nome_monitor": "Iago",
    "tipo_mensagem": "Elogio",
    "texto_feedback": "A persistência está funcionando!",
    "data_submissao": datetime.now(),  # Alterado para objeto datetime nativo
    "hash_aluno": "hash123",
}

id_gerado = repo.insert(dados_exemplo)
print(f"Feedback inserido com ID: {id_gerado}")

# 3. Testando o COUNT
print("\n--- Testando COUNT ---")
total_registros = repo.count()
print(f"Total de registros no banco: {total_registros}")

# 4. Testando o GET_BY_ID (ID Válido)
print("\n--- Testando GET_BY_ID (ID Válido) ---")
registro_encontrado = repo.get_by_id(id_gerado)
print(f"Busca pelo ID {id_gerado}: {registro_encontrado}")

# 5. Testando o GET_BY_ID (ID Inválido)
print("\n--- Testando GET_BY_ID (ID Inválido) ---")
registro_nao_encontrado = repo.get_by_id(9999)
print(f"Busca pelo ID 9999: {registro_nao_encontrado}")

# 6. Testando o READ
print("\n--- Lendo dados do Delta Lake em Lotes ---")
for batch in repo.read(batch_size=1):
    for registro in batch:
        print(f"Registro do lote: {registro}")

# 7. Testando o VACUUM
print("\n--- Rodando faxina (Vacuum) ---")
# Passando os parâmetros para forçar a limpeza imediata no ambiente de teste
repo.vacuum(retention_hours=0, enforce_retention_duration=False)
print("Teste finalizado com sucesso!")
