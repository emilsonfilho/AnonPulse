import os
from filelock import FileLock

class SequenceManager:
    def __init__(self, file_path: str):
        
        self.file_path = file_path
        
        self.lock_path = f"{file_path}.lock"

    def get_next_id(self) -> int:
        
        with FileLock(self.lock_path):
            
            # Verifica se o arquivo já existe
            if not os.path.exists(self.file_path):
                current_id = 0
            else:
                # Abre em modo de leitura ("r"), lê o conteúdo e converte para inteiro
                with open(self.file_path, "r") as f:
                    content = f.read().strip()
                    # Se por acaso o arquivo estiver vazio, assume 0, senão converte o texto para int
                    if content:
                        current_id = int(content)
                    else:
                        current_id = 0

            # Faz o incremento em memória
            next_id = current_id + 1

            # Abre em modo de escrita ("w") para sobrescrever o arquivo com o novo valor
            with open(self.file_path, "w") as f:
                f.write(str(next_id))

            return next_id
