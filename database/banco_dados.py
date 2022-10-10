import sqlite3 as sql


class BancoDados:
    def __init__(self):
        self.__con = sql.connect("./database/dashboard.db")
        self.__cur = self.__con.cursor()

    def finalizar(self):
        self.__cur.close()
        self.__con.close()

    def entregas_busca(self, id_entrega):
        self.__cur.execute("SELECT * FROM ENTREGAS WHERE id=?", [str(id_entrega)])
        return self.__cur.fetchone()

    def entregas_lista(self):
        self.__cur.execute("SELECT * FROM ENTREGAS")
        return self.__cur.fetchall()

    def entregas_andamento(self):
        self.__cur.execute("SELECT * FROM ENTREGAS WHERE status='Em andamento...'")
        return self.__cur.fetchall()

    def veiculos_busca(self, placa):
        self.__cur.execute("SELECT * FROM VEICULO WHERE placa=?", [placa])
        return self.__cur.fetchone()

    def veiculos_lista(self):
        self.__cur.execute("SELECT * FROM VEICULO")
        return self.__cur.fetchall()

    def veiculos_entregas(self, placa):
        self.__cur.execute("SELECT * FROM ENTREGAS WHERE placa=?", [placa])
        return self.__cur.fetchall()
