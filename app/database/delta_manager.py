import os

import pyarrow as pa
from deltalake import DeltaTable, write_deltalake

from app.database.seq_manager import SequenceManager

class FeedbackRepository:
    def __init__(self, table_path: str):
        self.table_path = table_path  # Pasta onde os arquivos Delta serão salvos

        os.makedirs(table_path, exist_ok=True)
        seq_file = os.path.join(table_path, "feedback.seq")
        self.seq_manager = SequenceManager(seq_file)

        self.schema = pa.schema(
            [
                ("id", pa.int64()),
                ("disciplina", pa.string()),
                ("nome_monitor", pa.string()),
                ("tipo_mensagem", pa.string()),
                ("texto_feedback", pa.string()),
                ("data_submissao", pa.timestamp("ms", tz="UTC")),
                ("hash_aluno", pa.string()),
            ]
        )

    @property
    def _tabela(self):
        caminho_log = os.path.join(self.table_path, "_delta_log")
        if not os.path.exists(caminho_log):
            return None
        return DeltaTable(self.table_path)

    def insert(self, dados: dict):
        new_id = self.seq_manager.get_next_id()

        dados_com_id = {**dados, "id": new_id}

        # Converter os dados para o formato necessário para criar uma tabela Delta
        dados_coluna = {chave: [valor] for chave, valor in dados_com_id.items()}
        tabela = pa.Table.from_pydict(dados_coluna, schema=self.schema)

        write_deltalake(self.table_path, tabela, mode="append")

        return new_id

    def read(self, batch_size: int = 100):
        if not self._tabela:
            return

        dataset = self._tabela.to_pyarrow_dataset()
        batches = dataset.to_batches(batch_size=batch_size)

        # Gerar os dados em lotes para evitar sobrecarregar a memória
        for pedaco in batches:
            yield pedaco.to_pylist()

    def delete(self, feedback_id: int):
        self._tabela.delete(predicate=f"id = {feedback_id}")

    def update(self, feedback_id: int, novos_dados: dict):
        dados_formatados = {}
        
        for k, v in novos_dados.items():
            # 1. Se for um Enum, pegamos apenas o texto dele (.value)
            # 2. Se não for Enum, mantemos o valor original
            valor_real = v.value if hasattr(v, "value") else v
            
            # 3. Se o resultado for uma string, colocamos as aspas simples pro Delta
            if isinstance(valor_real, str):
                dados_formatados[k] = f"'{valor_real}'"
            else:
                dados_formatados[k] = valor_real

        # Executa o update com os dados limpos
        self._tabela.update(
            predicate=f"id = {feedback_id}",
            updates=dados_formatados
        )

    # Método para limpeza de arquivos antigos e otimização do armazenamento
    def vacuum(
        self, retention_hours: int = 168, enforce_retention_duration: bool = True
    ):
        self._tabela.vacuum(
            retention_hours=retention_hours,
            enforce_retention_duration=enforce_retention_duration,
        )

    def get_by_id(self, feedback_id: int) -> dict | None:
        dados = self._tabela.to_pyarrow_table(
            filters=[("id", "=", feedback_id)]
        ).to_pydict()

        if dados["id"]:
            return {chave: valor[0] for chave, valor in dados.items()}
        else:
            return None

    def count(self) -> int:
        return self._tabela.to_pyarrow_dataset().count_rows()
