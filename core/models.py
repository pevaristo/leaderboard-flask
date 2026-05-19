from datetime import datetime

class TimestampModel:
    """
    Classe base de criação e modificação nos modelos.
    """
    def __init__(self, created_at=None, updated_at=None):
        # Se for um novo registro, gera o timestamp atual em UTC.
        # Caso esteja vindo do banco, preserva o valor existente.
        agora = datetime.utcnow().isoformat()
        self.created_at = created_at if created_at else agora
        self.updated_at = updated_at if updated_at else agora

    def registrar_atualizacao(self):
        self.updated_at = datetime.utcnow().isoformat()


class Match(TimestampModel):
    def __init__(self, nickname, score, seconds=0, text="", id=None, created_at=None, updated_at=None):
        # Inicializa a classe base para gerenciar as datas
        super().__init__(created_at, updated_at)
        
        # O ID começa como None para novos registros e recebe o valor numérico do banco na listagem
        self.id = id
        self.nickname = nickname
        self.score = score
        self.seconds = seconds
        self.text = text

    def to_dict(self):
        """Converte o objeto em dicionário para facilitar o retorno em JSON na API."""
        return {
            "id": self.id,
            "nickname": self.nickname,
            "score": self.score,
            "seconds": self.seconds,
            "text": self.text,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }