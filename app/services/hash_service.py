from hashlib import md5, sha1, sha256
from api.core.enums import HashAlgorithm


class HashService:
    algorithms = {
        HashAlgorithm.MD5: md5,
        HashAlgorithm.SHA1: sha1,
        HashAlgorithm.SHA256: sha256,
    }

    @staticmethod
    def generate_hash(text: str, algorithm: HashAlgorithm) -> str:
        if algorithm in HashService.algorithms:
            return HashService.algorithms[algorithm](text.encode()).hexdigest()
        else:
            raise ValueError("Algoritmo de hash não suportado.")
