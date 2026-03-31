from enum import Enum


class MessageType(str, Enum):
    ELOGIO = "Elogio"
    CRITICA = "Crítica"
    DUVIDA = "Dúvida"
    SUGESTAO = "Sugestão"
