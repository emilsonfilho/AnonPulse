from hashlib import md5, sha1, sha256, sha3_256, blake2b
from app.api.core.enums import HashAlgorithm


class HashService:
    algorithms = {
        HashAlgorithm.MD5: md5,
        HashAlgorithm.SHA1: sha1,
        HashAlgorithm.SHA256: sha256,
        HashAlgorithm.SHA3_256: sha3_256,
        HashAlgorithm.BLAKE2B: blake2b,
    }

    @classmethod
    def get_algorithm(cls, algorithm: HashAlgorithm):
        try:
            return cls.algorithms[algorithm]
        except KeyError:
            raise ValueError(f"Algoritmo não suportado: {algorithm}")

    @staticmethod
    def generate_hash(text: str, algorithm: HashAlgorithm) -> str:
        hasher = HashService.get_algorithm(algorithm)()
        hasher.update(text.encode())
        return hasher.hexdigest()
