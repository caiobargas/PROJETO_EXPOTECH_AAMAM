import mysql.connector
from mysql.connector import Error


def conectar():
    try:
        conexao = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='310805Cv@',
            database='expotec_aamam',
            auth_plugin='mysql_native_password'
        )

        if conexao.is_connected():
            print("Conectado ao MySQL com sucesso!")
            return conexao

    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None


def fechar_conexao(conexao):
    if conexao and conexao.is_connected():
        conexao.close()
        print("ConexÃ£o encerrada.")


conexao = conectar()
