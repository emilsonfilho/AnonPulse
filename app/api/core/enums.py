from enum import Enum


class MessageType(str, Enum):
    ELOGIO = "Elogio"
    CRITICA = "Crítica"
    DUVIDA = "Dúvida"
    SUGESTAO = "Sugestão"


class HashAlgorithm(str, Enum):
    MD5 = "MD5"
    SHA1 = "SHA-1"
    SHA256 = "SHA-256"
