"""Módulo de serviço para geração de hashes criptográficos.

Este módulo fornece funcionalidades para gerar hashes usando diferentes
algoritmos criptográficos suportados.
"""
from hashlib import blake2b, md5, sha1, sha3_256, sha256

from app.core.enums import HashAlgorithm


class HashService:
    """Serviço para manipulação e geração de hashes criptográficos.
    
    Esta classe fornece métodos para obter algoritmos de hash suportados
    e gerar hashes a partir de texto usando o algoritmo especificado.
    """

    _algorithms = {
        HashAlgorithm.MD5: md5,
        HashAlgorithm.SHA1: sha1,
        HashAlgorithm.SHA256: sha256,
        HashAlgorithm.SHA3_256: sha3_256,
        HashAlgorithm.BLAKE2B: blake2b,
    }

    @classmethod
    def get_algorithm(cls, algorithm: HashAlgorithm):
        """Obtém a função de hash correspondente ao algoritmo.
        
        Args:
            algorithm: Enumeração do algoritmo de hash desejado.
            
        Returns:
            Função do algoritmo de hash correspondente.
            
        Raises:
            ValueError: Se o algoritmo não for suportado.
        """
        try:
            return cls._algorithms[algorithm]
        except KeyError:
            raise ValueError(f"Algoritmo não suportado: {algorithm}")

    @staticmethod
    def generate_hash(text: str, algorithm: HashAlgorithm) -> str:
        """Gera um hash criptográfico para o texto fornecido.
        
        Args:
            text: Texto para o qual gerar o hash.
            algorithm: Algoritmo de hash a ser utilizado.
            
        Returns:
            String hexadecimal representando o hash gerado.
        """
        hasher = HashService.get_algorithm(algorithm)()
        hasher.update(text.encode())
        return hasher.hexdigest()
