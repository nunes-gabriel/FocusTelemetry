import sqlite3 as sql


class BancoDados:
    def __init__(self):
        self.__con = sql.connect("./database/dashboard.db")
        self.__cur = self.__con.cursor()

    def finalizar(self):
        self.__cur.close()
        self.__con.close()

    """
    >>> Tabela de Entregas
    """
    def entregas_lista(self):
        self.__cur.execute("SELECT * FROM ENTREGAS")
        return self.__cur.fetchall()

    def entregas_busca(self, id_entrega):
        self.__cur.execute("SELECT * FROM ENTREGAS WHERE id=?", [str(id_entrega)])
        return self.__cur.fetchone()

    def entregas_andamento(self):
        self.__cur.execute("SELECT * FROM ENTREGAS WHERE status='Em andamento...'")
        return self.__cur.fetchall()

    """
    >>> Tabela de Veículos
    """
    def veiculos_lista(self):
        self.__cur.execute("SELECT * FROM VEICULO")
        return self.__cur.fetchall()

    def veiculos_placas(self):
        self.__cur.execute("SELECT placa FROM VEICULO")
        return self.__cur.fetchall()

    def veiculos_busca(self, placa):
        self.__cur.execute("SELECT * FROM VEICULO WHERE placa=?", [placa])
        return self.__cur.fetchone()

    def veiculos_criar(self, colunas):
        self.__cur.execute("""
            INSERT INTO VEICULO(Placa, Marca, Tipo_de_Veículo, Cor, Renavam, Ano, Tipo_Carroceria, Altura, Largura,
            Comprimento, Tara_KG, Capacidade_em_KG, Vencimento_do_Documento, Feedback_do_Veículo)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, colunas + ["Disponível"])
        self.__con.commit()

    def veiculos_atualizar(self, placa, colunas):
        self.__cur.execute(f"""
            UPDATE VEICULO
            SET Marca=?, Tipo_de_Veículo=?, Cor=?, Renavam=?, Ano=?, Tipo_Carroceria=?, Altura=?,
            Largura=?, Comprimento=?, Tara_KG=?, Capacidade_em_KG=?, Vencimento_do_Documento=?
            WHERE placa='{placa}'
            """, colunas)
        self.__con.commit()

    def veiculos_deletar(self, placa):
        self.__cur.execute("DELETE FROM VEICULO WHERE placa=?", [placa])
        self.__con.commit()

    """
    >>> Tabela de Motoristas
    """
    def motoristas_lista(self):
        self.__cur.execute("SELECT * FROM MOTORISTA")
        return self.__cur.fetchall()

    def motoristas_identidade(self):
        self.__cur.execute("SELECT rg, cpf FROM MOTORISTA")
        return self.__cur.fetchall()

    def motoristas_busca(self, cpf):
        self.__cur.execute("SELECT * FROM MOTORISTA WHERE cpf=?", [cpf])
        return self.__cur.fetchone()

    def motoristas_criar(self, colunas):
        self.__cur.execute("""
            INSERT INTO MOTORISTA(Nome, Idade, RG, CPF, Telefone, CEP, Rua, Número, Cidade, Estado,
            Registro_Habilitação, Categoria_Habilitação)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, colunas)
        self.__con.commit()

    def motoristas_atualizar(self, cpf, colunas):
        self.__cur.execute(f"""
            UPDATE MOTORISTA
            SET Nome=?, Idade=?, Telefone=?, CEP=?, Rua=?, Número=?, Cidade=?, Estado=?, Registro_Habilitação=?,
            Categoria_Habilitação=?
            WHERE cpf='{cpf}'
            """, colunas)
        self.__con.commit()

    def motoristas_deletar(self, cpf):
        self.__cur.execute("DELETE FROM MOTORISTA WHERE cpf=?", [cpf])
        self.__con.commit()
