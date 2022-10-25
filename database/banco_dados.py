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

    def entregas_id(self):
        self.__cur.execute("SELECT seq FROM sqlite_sequence WHERE name='ENTREGAS'")
        return int(self.__cur.fetchone()[0]) + 1

    def entregas_tamanho(self):
        self.__cur.execute("SELECT COUNT(*) AS NUM FROM ENTREGAS")
        return self.__cur.fetchone()[0]

    def entregas_veiculo(self, placa):
        self.__cur.execute("SELECT id FROM ENTREGAS WHERE Placa=? AND Status IN ('Não Entregue', 'Não Entregue ')", [placa])
        return self.__cur.fetchone()

    def entregas_motorista(self, cpf):
        self.__cur.execute("SELECT id FROM ENTREGAS WHERE CPF_Motorista=? AND Status IN ('Não Entregue', 'Não Entregue ')", [cpf])
        return self.__cur.fetchone()

    def entregas_busca(self, id_entrega):
        self.__cur.execute("SELECT * FROM ENTREGAS WHERE id=?", [str(id_entrega)])
        return self.__cur.fetchone()

    def entregas_criar(self, colunas):
        self.__cur.execute("""
            INSERT INTO ENTREGAS(Placa, CPF_Motorista, Origem, Destino, Tipo_de_Carga, Quantidade_em_KG, Valor_da_Carga, Parada,
            Data_de_Saida, Data_Prevista, Data_de_Chegada, Status, Feedback_detalhado)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, colunas)
        self.__con.commit()

    def entregas_data_saida(self, id_entrega, coluna):
        self.__cur.execute("UPDATE ENTREGAS SET Data_de_saida=? WHERE id=?", [coluna, id_entrega])
        self.__con.commit()
    
    def entregas_data_prevista(self, id_entrega, coluna):
        self.__cur.execute("UPDATE ENTREGAS SET Data_Prevista=? WHERE id=?", [coluna, id_entrega])
        self.__con.commit()

    def entregas_data_chegada(self, id_entrega, coluna):
        self.__cur.execute("UPDATE ENTREGAS SET Data_de_Chegada=? WHERE id=?", [coluna, id_entrega])
        self.__con.commit()

    def entregas_status(self, id_entrega, coluna):
        self.__cur.execute("UPDATE ENTREGAS SET Status=? WHERE id=?", [coluna, id_entrega])
        self.__con.commit()

    def entregas_feedback(self, id_entrega, coluna):
        self.__cur.execute("UPDATE ENTREGAS SET Feedback_detalhado=? WHERE id=?", [coluna, id_entrega])
        self.__con.commit()

    def entregas_ocupar(self, id_entrega):
        self.__cur.execute("""
            UPDATE VEICULO SET Feedback_do_Veículo='Em Viagem' WHERE Placa IN (SELECT Placa FROM ENTREGAS WHERE id=? AND Status IN ('Não Entregue', 'Não Entregue '))
            """, [id_entrega])
        self.__cur.execute("""
            UPDATE MOTORISTA SET Status='Em Viagem' WHERE CPF IN (SELECT CPF_Motorista FROM ENTREGAS WHERE id=? AND Status IN ('Não Entregue', 'Não Entregue '))
            """, [id_entrega])
        self.__con.commit()

    def entregas_desocupar(self, id_entrega):
        self.__cur.execute("""
            UPDATE VEICULO SET Feedback_do_Veículo='Disponível' WHERE Placa IN (SELECT Placa FROM ENTREGAS WHERE id=? AND Status IN ('Não Entregue', 'Não Entregue '))
            """, [id_entrega])
        self.__cur.execute("""
            UPDATE MOTORISTA SET Status='Disponível' WHERE CPF IN (SELECT CPF_Motorista FROM ENTREGAS WHERE id=? AND Status IN ('Não Entregue', 'Não Entregue '))
            """, [id_entrega])
        self.__con.commit()

    def entregas_andamento(self):
        self.__cur.execute("SELECT * FROM ENTREGAS WHERE status='Em andamento...'")
        return self.__cur.fetchall()

    def entregas_deletar(self, id_entrega):
        self.__cur.execute("DELETE FROM ENTREGAS WHERE id=?", [id_entrega])
        self.__con.commit()

    """
    >>> Tabela de Veículos
    """
    def veiculos_lista(self):
        self.__cur.execute("SELECT * FROM VEICULO")
        return self.__cur.fetchall()

    def veiculos_disponiveis(self):
        self.__cur.execute("SELECT placa, marca FROM VEICULO WHERE Feedback_do_Veículo IN ('Disponível', 'Disponível ')")
        return self.__cur.fetchall()

    def veiculos_tamanho(self):
        self.__cur.execute("SELECT COUNT(*) AS NUM FROM VEICULO")
        return self.__cur.fetchone()[0]

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
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Disponível')
            """, colunas)
        self.__con.commit()

    def veiculos_atualizar(self, placa, colunas):
        self.__cur.execute(f"""
            UPDATE VEICULO
            SET Marca=?, Tipo_de_Veículo=?, Cor=?, Renavam=?, Ano=?, Tipo_Carroceria=?, Altura=?,
            Largura=?, Comprimento=?, Tara_KG=?, Capacidade_em_KG=?, Vencimento_do_Documento=?
            WHERE placa='{placa}'
            """, colunas)
        self.__con.commit()

    def veiculos_status(self, placa, coluna):
        self.__cur.execute("UPDATE VEICULO SET Feedback_do_Veículo=? WHERE placa=?", [coluna, placa])
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

    def motoristas_disponiveis(self):
        self.__cur.execute("SELECT nome, cpf FROM MOTORISTA WHERE Status IN ('Disponível', 'Disponível ')")
        return self.__cur.fetchall()

    def motoristas_tamanho(self):
        self.__cur.execute("SELECT COUNT(*) AS NUM FROM MOTORISTA")
        return self.__cur.fetchone()[0]

    def motoristas_identidade(self):
        self.__cur.execute("SELECT rg, cpf FROM MOTORISTA")
        return self.__cur.fetchall()

    def motoristas_busca(self, cpf):
        self.__cur.execute("SELECT * FROM MOTORISTA WHERE cpf=?", [cpf])
        return self.__cur.fetchone()

    def motoristas_criar(self, colunas):
        self.__cur.execute("""
            INSERT INTO MOTORISTA(Nome, Idade, RG, CPF, Telefone, CEP, Rua, Número, Cidade, Estado,
            Registro_Habilitação, Categoria_Habilitação, Status)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Disponível')
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

    def motoristas_status(self, cpf, coluna):
        self.__cur.execute("UPDATE MOTORISTA SET Status=? WHERE cpf=?", [coluna, cpf])
        self.__con.commit()

    def motoristas_deletar(self, cpf):
        self.__cur.execute("DELETE FROM MOTORISTA WHERE cpf=?", [cpf])
        self.__con.commit()
