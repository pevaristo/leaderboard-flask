from datetime import datetime, timezone, timedelta
from core.leaderboard import Leaderboard
from core.models import Match


def data_local_filter(data_iso_str):
    """Filtro para converter string ISO UTC para o formato em UTC -03:00"""
    if not data_iso_str:
        return ""
    try:
        dt_utc = datetime.fromisoformat(data_iso_str).replace(tzinfo=timezone.utc)
        fuso_local = timezone(timedelta(hours=-3))
        dt_local = dt_utc.astimezone(fuso_local)
        return dt_local.strftime('%d/%m/%Y às %H:%M:%S')
    except Exception:
        return data_iso_str


def seed_inicial(dao):
    """Verifica se o banco está vazio e popula com os dados do leaderboard.py"""
    if len(dao.listar_todos()) == 0:
        print("Banco de dados vazio. Iniciando carga a partir de leaderboard.py...")
        for item in Leaderboard:
            nova_partida = Match(
                nickname=item["nickname"],
                score=int(item["score"]),
                seconds=int(item["seconds"]),
                text=item["text"]
            )
            dao.inserir(nova_partida)
        print("Carga inicial concluída com sucesso!")