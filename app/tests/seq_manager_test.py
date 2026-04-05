import os

from app.database.seq_manager import SequenceManager


def main():
    # descobre o caminho do diretório
    dir_atual = os.path.dirname(__file__)
    path = os.path.join(dir_atual, "data_test")

    # Cria uma pasta temporária na raiz do projeto para os arquivos de teste
    os.makedirs(path, exist_ok=True)
    caminho_arquivo = os.path.join(path, "teste_externo.seq")

    # Instancia a classe
    print("Iniciando o teste do Gerenciador de Sequência...")
    gerenciador = SequenceManager(caminho_arquivo)

    # Loop para simular 5 criações
    for i in range(1, 6):
        novo_id = gerenciador.get_next_id()
        print(f"Tentativa {i}: O ID gerado foi {novo_id}")

    print("Teste concluído com sucesso!")


if __name__ == "__main__":
    main()
