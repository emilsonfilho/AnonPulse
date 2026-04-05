from hashlib import blake2b, md5, sha1, sha3_256, sha256

from app.api.core.enums import HashAlgorithm


class HashService:
    _algorithms = {
        HashAlgorithm.MD5: md5,
        HashAlgorithm.SHA1: sha1,
        HashAlgorithm.SHA256: sha256,
        HashAlgorithm.SHA3_256: sha3_256,
        HashAlgorithm.BLAKE2B: blake2b,
    }

    @classmethod
    def get_algorithm(cls, algorithm: HashAlgorithm):
        try:
            return cls._algorithms[algorithm]
        except KeyError:
            raise ValueError(f"Algoritmo não suportado: {algorithm}")

    @staticmethod
    def generate_hash(text: str, algorithm: HashAlgorithm) -> str:
        hasher = HashService.get_algorithm(algorithm)()
        hasher.update(text.encode())
        return hasher.hexdigest()
