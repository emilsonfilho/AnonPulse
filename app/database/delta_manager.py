import os

import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

from app.database.seq_manager import SequenceManager

class FeedbackRepository:

    def __init__(self, table_path: str):
        self.table_path = table_path # Pasta onde os arquivos Delta serão salvos

        os.makedirs(table_path, exist_ok=True)
        seq_file = os.path.join(table_path, "feedback.seq")
        self.seq_manager = SequenceManager(seq_file)

        self.schema = pa.schema([
            ("id", pa.int64()),
            ("disciplina", pa.string()),
            ("nome_monitor", pa.string()),
            ("tipo_mensagem", pa.string()),
            ("texto_feedback", pa.string()),
            ("data_submissao", pa.string()),
            ("hash_aluno", pa.string())
        ])

    def insert(self, dados: dict):
        new_id = self.seq_manager.get_next_id()

        dados_com_id = {**dados, "id": new_id}

        # Converter os dados para o formato necessário para criar uma tabela Delta
        dados_coluna = {chave: [valor] for chave, valor in dados_com_id.items()}
        tabela = pa.Table.from_pydict(dados_coluna, schema=self.schema)

        write_deltalake(self.table_path, tabela, mode="append")

        return new_id
    
    def read(self, batch_size: int = 100):
     
        tabela_delta = DeltaTable(self.table_path)

        dataset = tabela_delta.to_pyarrow_dataset()
        batches = dataset.to_batches(batch_size=batch_size)

        # Gerar os dados em lotes para evitar sobrecarregar a memória
        for pedaco in batches:
            yield pedaco.to_pylist()

    def delete(self, feedback_id: int):
        tabela = DeltaTable(self.table_path)

        tabela.delete(condition=f"id = {feedback_id}")

    def update(self, feedback_id: int, novos_dados: dict):
        tabela = DeltaTable(self.table_path)
        tabela.update(
            condition=f"id = {feedback_id}",
            updates=novos_dados
        )
    
    # Método para limpeza de arquivos antigos e otimização do armazenamento
    def vacuum(self):
        tabela = DeltaTable(self.table_path)
        
        # Tempo para deleção completa definido momentaneamente como 0h
        tabela.vacuum(retention_hours=0, enforce_retention_duration=False)