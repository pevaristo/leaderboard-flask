import sqlite3
from sqlite3 import Error
from core.models import Match

class LeaderboardDAO:
    def __init__(self, db_file="banco.db"):
        self.db_file = db_file

    def _conectar(self):
        try:
            return sqlite3.connect(self.db_file)
        except Error as e:
            print(f"Erro ao conectar ao banco SQLite: {e}")
            return None

    def criar_tabela(self):
        sql = """
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT NOT NULL,
            score INTEGER NOT NULL,
            seconds INTEGER,
            text TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
            except Error as e:
                print(f"Erro ao criar a tabela leaderboard: {e}")
            finally:
                conn.close()

    def inserir(self, match):
        """Insere uma nova partida no banco e injeta o ID gerado de volta no objeto Match."""
        sql = """INSERT INTO leaderboard (nickname, score, seconds, text, created_at, updated_at) 
                 VALUES (?, ?, ?, ?, ?, ?)"""
        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, (
                    match.nickname, 
                    match.score, 
                    match.seconds, 
                    match.text, 
                    match.created_at, 
                    match.updated_at
                ))
                conn.commit()
                # Captura o ID numérico gerado pelo AUTOINCREMENT e salva no objeto
                match.id = cursor.lastrowid
                return match.id
            except Error as e:
                print(f"Erro ao inserir registro: {e}")
                return None
            finally:
                conn.close()

    def listar_todos(self):
        sql = "SELECT id, nickname, score, seconds, text, created_at, updated_at FROM leaderboard ORDER BY score DESC"
        conn = self._conectar()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            # Mapeia as colunas do banco ordenadamente para o construtor da classe Match
            return [
                Match(
                    id=r[0], 
                    nickname=r[1], 
                    score=r[2], 
                    seconds=r[3], 
                    text=r[4], 
                    created_at=r[5], 
                    updated_at=r[6]
                ) for r in rows
            ]
        except Error as e:
            print(f"Erro ao listar o placar: {e}")
            return []
        finally:
            conn.close()

    def buscar_por_id(self, entry_id):
        sql = "SELECT id, nickname, score, seconds, text, created_at, updated_at FROM leaderboard WHERE id = ?"
        conn = self._conectar()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (entry_id,))
            r = cursor.fetchone()
            if r:
                return Match(
                    id=r[0], nickname=r[1], score=r[2], seconds=r[3], 
                    text=r[4], created_at=r[5], updated_at=r[6]
                )
            return None
        except Error as e:
            print(f"Erro ao buscar registro por ID: {e}")
            return None
        finally:
            conn.close()

    def atualizar(self, match):
        # Força a atualização da data
        match.registrar_atualizacao()
        
        sql = """UPDATE leaderboard 
                 SET nickname = ?, score = ?, seconds = ?, text = ?, updated_at = ? 
                 WHERE id = ?"""
        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, (
                    match.nickname, 
                    match.score, 
                    match.seconds, 
                    match.text, 
                    match.updated_at, 
                    match.id
                ))
                conn.commit()
                return cursor.rowcount
            except Error as e:
                print(f"Erro ao atualizar registro: {e}")
                return 0
            finally:
                conn.close()

    def deletar(self, entry_id):
        sql = "DELETE FROM leaderboard WHERE id = ?"
        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, (entry_id,))
                conn.commit()
                return cursor.rowcount
            except Error as e:
                print(f"Erro ao deletar registro: {e}")
                return 0
            finally:
                conn.close()