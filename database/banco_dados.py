import sqlite3 as sql


class BancoDados:
    def __init__(self):
        self.__con = sql.connect("./database/dashboard.db")
        self.__cur = self.__con.cursor()

    def finalizar(self):
        self.__cur.close()
        self.__con.close()

    def entregas_busca(self, id_entrega):
        self.__cur.execute("SELECT * FROM Entregas WHERE id=?", [str(id_entrega)])
        return self.__cur.fetchone()

    def entregas_lista(self):
        self.__cur.execute("SELECT * FROM Entregas")
        return self.__cur.fetchall()
