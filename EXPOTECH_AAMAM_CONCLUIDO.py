
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from conexao import conectar, fechar_conexao
import re

# =========================
# USUÁRIOS
# =========================


def adicionar_usuario(conexao):

    print("\n=== USUÁRIOS CADASTRADOS ===")
    listar_usuarios(conexao)

    nome_usuario = input("\nDigite o nome do usuário: ").strip()

    if not nome_usuario:
        print("Nome inválido.")
        return

    while True:
        dt_nasc_usuario = input(
            "Digite a data de nascimento do usuário (YYYY-MM-DD): ")
        try:
            datetime.strptime(dt_nasc_usuario, "%Y-%m-%d")
            break
        except:
            print("Data inválida, por favor inserir uma data válida")

    email_usuario = input("Digite o email do usuário: ").strip()
    padrao = r'^[\w.-]+@[\w.-]+.\w+$'

    if not re.match(padrao, email_usuario):
        print("E-mail inválido!")
        return

    data_cadastro_usuario = datetime.now().date()
    if not data_cadastro_usuario:
        print("Data inválida")
        return

    usuario_ativo = input("Ativo? [S/N]: ").strip().upper()
    usuario_ativo = 1 if usuario_ativo == 'S' else 0

    genero_usuario = input(
        "Digite o genero do usuário Masculino ou Feminino: ").strip().capitalize()

    if genero_usuario not in ['Feminino', 'Masculino']:
        print("Genero inválido")
        return

    cursor = conexao.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios
            (nome_usuario, dt_nasc_usuario, email_usuario, data_cadastro_usuario, usuario_ativo, genero_usuario)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (nome_usuario, dt_nasc_usuario, email_usuario, datetime.now().date(), usuario_ativo, genero_usuario))

        conexao.commit()
        print("Usuário cadastrado!")

    except mysql.connector.Error:
        print("Não foi possível cadastrar o usuário.")


def adicionar_usuario_tratamento(conexao):
    print("\n=== USUÁRIOS CADASTRADOS ===")
    listar_usuarios(conexao)

    id_usuario = input("\nDigite o ID do usuário: ").strip()

    if not id_usuario.isdigit():
        print("ID inválido.")
        return

    id_tratamento = input("Digite o ID do tratamento: ").strip()

    if not id_tratamento.isdigit():
        print("ID do tratamento inválido.")
        return

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            UPDATE tratamentos
            SET fk_tratamento_usuarios = %s
            WHERE id_tratamento = %s
            """,
            (id_usuario, id_tratamento)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("Usuário não encontrado.")
        else:
            print("Usuário vinculado ao tratamento com sucesso!")

    except ValueError:
        print("Digite apenas números inteiros para os IDs.")

    except Exception as erro:
        print(f"Erro ao associar usuário ao tratamento: {erro}")

        cursor.close()


def listar_usuarios(conexao):
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
    SELECT id_usuario, nome_usuario, dt_nasc_usuario, email_usuario, data_cadastro_usuario, usuario_ativo, genero_usuario
        FROM usuarios
        ORDER BY id_usuario
            """)

    usuarios = cursor.fetchall()

    if not usuarios:
        print("Nenhum usuário cadastrado no momento.")
        return

    for usuario in usuarios:
        print(
            f"\n [{usuario['id_usuario']}]"
            f"\n nome do usuário:  [{usuario['nome_usuario']}] "
            f"\n data de nascimento do usuário:  [{usuario['dt_nasc_usuario']}] "
            f"\n email cadastrado do usuário:  [{usuario['email_usuario']}] "
            f"\n data de cadastro do usuário:  [{usuario['data_cadastro_usuario']}] "
            f"\n status do usuário:  [Ativo: {usuario['usuario_ativo']}] "
            f"\n gênero do usuário:  [{usuario['genero_usuario']}]\n"
        )


def listar_usuarios_tratamentos(conexao):

    cursor = conexao.cursor()

    try:

        cursor.execute("""
            SELECT 
                u.id_usuario,
                u.nome_usuario,
                t.nome_tratamento,
                t.descricao_tratamento,
                t.tipo_tratamento,
                t.inicio_tratamento,
                t.duracao_tratamento
            FROM usuarios u
            INNER JOIN tratamentos t
                ON u.id_usuario = t.fk_tratamento_usuarios
            ORDER BY u.id_usuario
        """)

        resultados = cursor.fetchall()

        if not resultados:
            print("Nenhum tratamento encontrado.")
            return

        print("\n=== USUÁRIOS E TRATAMENTOS ===")

        for tratamento in resultados:
            print(f"""
        \n ID Usuário: {tratamento[0]}
        \n Nome Usuário: {tratamento[1]}
        \n Nome Tratamento: {tratamento[2]}
        \n Descrição: {tratamento[3]}
        \n Tipo: {tratamento[4]}
        \n Início: {tratamento[5]}
        \n Duração: {tratamento[6]}\n
        """)

    except mysql.connector.Error as erro:
        print(f"Erro ao listar tratamentos dos usuários: {erro}")


def atualizar_usuario(conexao):

    print("\n=== USUÁRIOS CADASTRADOS ===")
    listar_usuarios(conexao)

    id_usuario = input("\nDigite o ID do usuário: ").strip()

    if not id_usuario.isdigit():
        print("ID inválido.")
        return

    novo_nome = input("Novo nome: ").strip()

    if not novo_nome:
        print("Nome inválido.")
        return

    nova_dt_nasc = input("Nova data nascimento (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(nova_dt_nasc, "%Y-%m-%d")
    except:
        print("Data inválida.")
        return

    novo_email = input("Novo email: ").strip()
    padrao = r'^[\w.-]+@[\w.-]+.\w+$'
    if not re.match(padrao, novo_email):
        print("E-mail inválido!")
        return

    if not novo_email:
        print("Email inválido.")
        return

    usuario_ativo = input("O usuário continua ativo? [S/N]").strip().upper()
    usuario_ativo = 1 if usuario_ativo == 'S' else 0

    genero_usuario = input(
        "Digite o seu novo genero: [Masculino / Feminino]").strip().capitalize()
    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            UPDATE usuarios
            SET nome_usuario = %s,dt_nasc_usuario = %s, email_usuario = %s, usuario_ativo = %s, genero_usuario = %s
            WHERE id_usuario = %s
            """,
            (novo_nome, nova_dt_nasc, novo_email,
             usuario_ativo, genero_usuario, id_usuario)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("Usuário não encontrado.")
        else:
            print("Usuário atualizado com sucesso!")

    except mysql.connector.Error:
        print("Não foi possível atualizar o usuário.")


# =========================
# CONTATOS DE EMERGÊNCIA
# =========================

def adicionar_contatoemergencia(conexao):

    print("\n=== CONTATOS DE EMERGÊNCIA ===")
    listar_contatoemergencia(conexao)

    nome = input("\nDigite o nome do contato de emergencia: ").strip()

    if not nome:
        print("Nome inválido.")
        return

    telefone = input("Digite o telefone do contato: ").strip()

    if not telefone:
        print("Telefone inválido.")
        return

    parentesco = input("Digite o parentesco: ").strip()

    if not parentesco:
        print("Parentesco inválido.")
        return

    fk_ce_usuario = input("Digite o ID do usuário: ").strip()

    if not fk_ce_usuario.isdigit():
        print("ID do usuário inválido")
        return

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO contato_emergencia (nome_contato, telefone_contato, parentesco, fk_ce_usuario)
            VALUES (%s, %s, %s, %s)
            """,
            (nome, telefone, parentesco, fk_ce_usuario)
        )

        conexao.commit()

        print("Contato de emergência cadastrado com sucesso!")

    except mysql.connector.Error:
        print("Não foi possível cadastrar o contato.")

    print(f"=======Lista de contatos de emergência atualizada=======")
    listar_contatoemergencia(conexao)


def listar_contatoemergencia(conexao):

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            ce.id_contato,
            ce.nome_contato,
            ce.telefone_contato,
            ce.parentesco,
            u.nome_usuario,
            u.id_usuario
        FROM contato_emergencia ce
        LEFT JOIN usuarios u 
            ON ce.fk_ce_usuario = u.id_usuario
        ORDER BY ce.id_contato
    """)

    contatos = cursor.fetchall()

    if not contatos:
        print("Nenhum contato de emergência cadastrado no momento.")
        return
    for contato in contatos:
        print(f"\n [{contato['id_contato']}] "
              f"\n nome do contato:  [{contato['nome_contato']}] "
              f"\n telefone do contato:  [{contato['telefone_contato']}] - "
              f"\n parentesco:  [{contato['parentesco']}] "
              f"\n nome do usuário:  [{contato['nome_usuario']}] "
              f"\n ID do usuário:  {contato['id_usuario']}\n "
              )


def atualizar_contatoemergencia(conexao):

    print("\n=== CONTATOS DE EMERGÊNCIA ===")
    listar_contatoemergencia(conexao)

    id_contato = input("\nDigite o ID do contato: ").strip()

    if not id_contato.isdigit():
        print("ID inválido.")
        return

    novo_nome = input("Novo nome do contato: ").strip()

    if not novo_nome:
        print("Nome inválido.")
        return

    novo_telefone = input("Novo telefone: ").strip()

    if not novo_telefone:
        print("Telefone inválido.")
        return

    novo_parentesco = input("Novo parentesco: ").strip()

    if not novo_parentesco:
        print("Parentesco inválido.")
        return

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            UPDATE contato_emergencia
            SET 
                nome_contato = %s,
                telefone_contato = %s,
                parentesco = %s
            WHERE id_contato = %s
            """,
            (novo_nome, novo_telefone, novo_parentesco, id_contato)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("Contato não encontrado.")
        else:
            print("Contato atualizado com sucesso!")

    except mysql.connector.Error:
        print("Não foi possível atualizar o contato.")

    # LISTA ATUALIZADA
    print("\n=== LISTA ATUALIZADA DE CONTATOS ===")
    listar_contatoemergencia(conexao)


def excluir_contatoemergencia(conexao):

    cursor = conexao.cursor()

    # Lista os contatos cadastrados
    cursor.execute("""
        SELECT contato_emergencia.id_contato, contato_emergencia.nome_contato, contato_emergencia.parentesco, 
                usuarios.id_usuario, usuarios.nome_usuario
        FROM contato_emergencia
        INNER JOIN usuarios ON contato_emergencia.fk_ce_usuario = usuarios.id_usuario
    """)

    contatos = cursor.fetchall()

    print("\n=== CONTATOS DE EMERGÊNCIA CADASTRADOS ===")

    if not contatos:
        print("Nenhum contato cadastrado.")
        return

    for contato in contatos:
        print(
            f"ID: {contato[0]} - Nome: {contato[1]} - Parentesco: {contato[2]} - Usuário: {contato[4]} (ID: {contato[3]})")

    # Solicita o ID do contato
    id_contato = int(input("\nDigite o ID do contato que deseja excluir: "))

    # Verifica se existe usuário vinculado ao contato
    cursor.execute("""
        SELECT fk_ce_usuario
        FROM contato_emergencia
        WHERE id_contato = %s
    """, (id_contato,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("Contato não encontrado.")
        return

    # Se houver usuário vinculado, não permite excluir
    if resultado[0] is not None:
        print("Não é possível excluir este contato.")
        print("Existe um usuário vinculado a este contato de emergência.")
        return

    # Exclui o contato
    try:
        cursor.execute("""
            DELETE FROM contato_emergencia
            WHERE id_contato = %s
        """, (id_contato,))

        conexao.commit()

        print("Contato de emergência excluído com sucesso!")

    except Exception as erro:
        print(f"Erro ao excluir contato: {erro}")

    finally:
        cursor.close()

# =========================
# REMÉDIOS
# =========================


def adicionar_remedio(conexao):

    print("\n=== Rémedios Cadastrados ===")
    listar_remedio(conexao)

    nome_remedio = input(
        "\nDigite o nome do remédio que deseja adicionar: ").strip().capitalize()

    if not nome_remedio:
        print("Nome do remédio inválido.")
        return

    descricao = input("Descrição do remédio: ").strip()
    if not descricao:
        print("descrição inválida")
        return

    dosagem = input("Digite a dosagem: ").strip()
    if not dosagem:
        print("Dosagem inválida.")
        return

    horario = input(
        "Digite o horário para tomar o remédio: ").strip()
    if not horario:
        print("Horário inválido.")
        return

    tipo_remedio = input("Digite o tipo do remédio: ").strip()

    if not tipo_remedio:
        print("Tipo inválido.")
        return

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO remedios (nome_remedio, descricao_remedio, dosagem_remedio, horario_remedio, tipo_remedio)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (nome_remedio, descricao, dosagem, horario, tipo_remedio)
        )

        conexao.commit()
        print("Remédio cadastrado com sucesso!")

    except mysql.connector.Error:
        print("Não foi possível cadastrar o remédio: ")


def listar_remedio(conexao):

    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        """SELECT id_remedio, nome_remedio, descricao_remedio, dosagem_remedio, horario_remedio, tipo_remedio FROM remedios ORDER BY id_remedio""")

    remedios = cursor.fetchall()

    if not remedios:
        print("Nenhum remédio cadastrado no momento.")
        return
    for remedio in remedios:
        print(
            f"\n [{remedio['id_remedio']}] "
            f"\n Nome remédio:  [{remedio['nome_remedio']}] "
            f"\n Descrição do remédio:  [{remedio['descricao_remedio']}] "
            f"\n Dosagem Recomenda do remédio:  [{remedio['dosagem_remedio']}] "
            f"\n Horário do remédio:  [{remedio['horario_remedio']}]"
            f"\n Tipo do remédio:  [{remedio['tipo_remedio']}] \n"
        )


def atualizar_remedio(conexao):

    print("\n=== REMÉDIOS CADASTRADOS ===")
    listar_remedio(conexao)

    id_remedio = input("\nDigite o ID do remédio: ").strip()

    if not id_remedio.isdigit():
        print("ID inválido.")
        return

    novo_nome = input("Novo nome do remédio: ").strip()

    if not novo_nome:
        print("Nome inválido.")
        return

    nova_dosagem = input("Nova dosagem: ").strip()

    if not nova_dosagem:
        print("Dosagem inválida.")
        return

    novo_horario = input("Novo horário: ").strip()

    if not novo_horario:
        print("Horário inválido.")
        return

    novo_tipo = input("Novo tipo do remédio: ").strip()

    if not novo_tipo:
        print("Tipo inválido.")
        return

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            UPDATE remedios
            SET nome_remedio = %s,
                dosagem_remedio = %s,
                horario_remedio = %s,
                tipo_remedio = %s
            WHERE id_remedio = %s
            """,
            (novo_nome, nova_dosagem, novo_horario, novo_tipo, id_remedio)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("Remédio não encontrado.")
        else:
            print("Remédio atualizado com sucesso!")

    except mysql.connector.Error:
        print("Não foi possível atualizar o remédio.")

    print(f"=======Lista de remédios atualizada=======")
    listar_remedio(conexao)


def excluir_remedio(conexao):

    print("\n=== REMÉDIOS CADASTRADOS ===")
    listar_remedio(conexao)

    id_remedio = input("\nDigite o ID do remédio que deseja excluir: ").strip()

    if not id_remedio.isdigit():
        print("ID inválido.")
        return

    confirmacao = input(
        "Tem certeza que deseja excluir? [S/N]: ").strip().upper()

    if confirmacao != 'S':
        print("Exclusão cancelada.")
        return

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """SELECT COUNT(*) FROM tratamentos WHERE fk_tratamento_remedios = %s""", (id_remedio,))

        if cursor.fetchone()[0] > 0:
            print(
                "Não é possível excluir o remédio, pois ele está cadastrado em um tratamento")
            return

        cursor.execute("""
            DELETE FROM remedios WHERE id_remedio = %s""", (id_remedio,))

        conexao.commit()
        print("Remédio excluído com sucesso")
    except mysql.connector.Error:
        print("Erro ao tentar excluir")

    finally:
        cursor.close()


# =========================
# TRATAMENTOS
# =========================

def adicionar_tratamento(conexao):

    print("\n=== TRATAMENTOS CADASTRADOS ===")
    listar_tratamentos(conexao)

    nome_tratamento = input("\nDigite o nome do tratamento: ").strip()

    if not nome_tratamento:
        print("Nome do tratamento inválido.")
        return

    descricao = input("Digite a descrição do tratamento: ").strip()

    if not descricao:
        print("Descrição inválida.")
        return

    tipo = input("Digite o tipo do tratamento: ").strip()

    if not tipo:
        print("Tipo inválido.")
        return

    while True:
        inicio_tratamento = input("Digite a data inicial (YYYY-MM-DD): ")
        try:
            datetime.strptime(inicio_tratamento, "%Y-%m-%d")
            break
        except:
            print("Data inválida, tente uma data valida")

    duracao = input("Digite a duração do tratamento: ").strip()

    if not duracao:
        print("Duração inválida.")
        return

    fk_remedio = input("Digite o ID do remédio: ").strip()

    if not fk_remedio.isdigit():
        print("ID do remédio inválido.")
        return

    data_cadastro = datetime.now().date()

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO tratamentos (nome_tratamento, descricao_tratamento, tipo_tratamento,inicio_tratamento, duracao_tratamento, data_cadastro_tratamento, fk_tratamento_remedios)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (nome_tratamento, descricao, tipo, inicio_tratamento,
             duracao, data_cadastro, fk_remedio)
        )

        conexao.commit()

        print("Tratamento cadastrado com sucesso!")

    except mysql.connector.Error:
        print("Não foi possível cadastrar o tratamento.")


def listar_tratamentos(conexao):

    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
    SELECT
        tratamentos.id_tratamento, tratamentos.nome_tratamento, tratamentos.tipo_tratamento, tratamentos.inicio_tratamento, tratamentos.descricao_tratamento, tratamentos.duracao_tratamento, remedios.nome_remedio
    FROM tratamentos 
    LEFT JOIN remedios 
        ON tratamentos.fk_tratamento_remedios = remedios.id_remedio
    ORDER BY tratamentos.id_tratamento
""")

    tratamentos = cursor.fetchall()

    if not tratamentos:
        print("Nenhum tratamento cadastrado no momento.")
        return

    for tratamento in tratamentos:
        print(
            f"\n [{tratamento['id_tratamento']}] "
            f"\n nome do tratamento:  [{tratamento['nome_tratamento']}] "
            f"\n tipo do tratamento:  [{tratamento['tipo_tratamento']}] "
            f"\n data de início:  [{tratamento['inicio_tratamento']}] "
            f"\n descrição do tratamento:  [{tratamento['descricao_tratamento']}] "
            f"\n duração do tratamento:  [{tratamento['duracao_tratamento']}] "
            f"\n remédio:  {tratamento['nome_remedio']} \n"
        )


def atualizar_tratamento(conexao):

    print("\n=== TRATAMENTOS CADASTRADOS ===")
    listar_tratamentos(conexao)

    id_tratamento = input("\nDigite o ID do tratamento: ").strip()

    if not id_tratamento.isdigit():
        print("ID inválido.")
        return

    novo_nome = input("Novo nome do tratamento: ").strip()

    if not novo_nome:
        print("Nome inválido.")
        return

    nova_descricao = input("Nova descrição: ").strip()

    if not nova_descricao:
        print("Descrição inválida.")
        return

    novo_tipo = input("Novo tipo: ").strip()

    if not novo_tipo:
        print("Tipo inválido.")
        return

    while True:
        inicio_tratamento = input("Digite a data inicial (YYYY-MM-DD): ")
        try:
            datetime.strptime(inicio_tratamento, "%Y-%m-%d")
            break
        except:
            print("Data inválida, tente uma data valida")

    nova_duracao = input("Nova duração: ").strip()

    if not nova_duracao:
        print("Duração inválida.")
        return

    novo_fk_remedio = input("Novo ID do remédio: ").strip()

    if not novo_fk_remedio.isdigit():
        print("ID do remédio inválido.")
        return

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            UPDATE tratamentos
            SET nome_tratamento = %s,
                descricao_tratamento = %s,
                tipo_tratamento = %s,
                inicio_tratamento = %s,
                duracao_tratamento = %s,
                fk_tratamento_remedios = %s
            WHERE id_tratamento = %s
            """,
            (novo_nome, nova_descricao, novo_tipo, inicio_tratamento,
             nova_duracao, novo_fk_remedio, id_tratamento)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("Tratamento não encontrado.")
        else:
            print("Tratamento atualizado com sucesso!")

    except mysql.connector.Error:
        print("Não foi possível atualizar o tratamento.")


def excluir_tratamento(conexao):

    cursor = conexao.cursor()

    # Lista os tratamentos cadastrados
    cursor.execute("""
        SELECT tratamentos.id_tratamento, tratamentos.nome_tratamento, tratamentos.tipo_tratamento, 
                remedios.id_remedio, remedios.nome_remedio
        FROM tratamentos
        INNER JOIN remedios ON tratamentos.fk_tratamento_remedios = remedios.id_remedio
        INNER JOIN usuarios ON tratamentos.fk_tratamento_usuarios = usuarios.id_usuario
    """)

    tratamentos = cursor.fetchall()
    print("\n=== TRATAMENTOS CADASTRADOS ===")

    if not tratamentos:
        print("Nenhum tratamento cadastrado.")
        return

    for tratamento in tratamentos:
        print(
            f"ID: {tratamento[0]} - Nome: {tratamento[1]} - Tipo: {tratamento[2]} - Remédio: {tratamento[4]} (ID: {tratamento[3]})")

    # Solicita o ID do tratamento
    id_tratamento = int(
        input("\nDigite o ID do tratamento que deseja excluir: "))

    # Verifica se existe remédio vinculado ao tratamento
    cursor.execute("""
        SELECT fk_tratamento_remedios, fk_tratamento_usuarios
        FROM tratamentos
        WHERE id_tratamento = %s
    """, (id_tratamento,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("Tratamento não encontrado.")
        return

    # Se houver remédio ou usuário vinculado, não permite excluir
    if resultado[0] is not None or resultado[1] is not None:
        print("Não é possível excluir este tratamento.")
        print("Existe um remédio ou um usuário vinculado a este tratamento.")
        return

    # Exclui o tratamento
    try:
        cursor.execute("""
            DELETE FROM tratamentos
            WHERE id_tratamento = %s
        """, (id_tratamento,))

        conexao.commit()

        print("Tratamento excluído com sucesso!")

    except Exception as erro:
        print(f"Erro ao excluir tratamento: {erro}")

    finally:
        cursor.close()


# =========================
# CONEXÃO
# =========================
conexao = conectar()

if conexao is None:
    print('Erro ao conectar com o banco de dados.')
    exit()


# =========================
# MENU PRINCIPAL
# =========================

try:
    while True:

        print('\n===== MENU PRINCIPAL =====')
        print('1 - Listar')
        print('2 - Adicionar')
        print('3 - Atualizar')
        print('4 - Excluir')
        print('5 - Sair')

        opcao = input('\nEscolha uma opção: ')

        # =========================
        # LISTAR
        # =========================
        if opcao == '1':

            print('\n===== LISTAR =====')
            print('1 - Usuários')
            print('2-  Usuários em Tratamentos')
            print('3 - Remédios')
            print('4 - Tratamentos')
            print('5 - Contatos de Emergência')
            print('6 - Voltar para o menu principal')

            escolha = input('\nEscolha uma opção: ')

            if escolha == '1':
                listar_usuarios(conexao)

            elif escolha == '2':
                listar_usuarios_tratamentos(conexao)

            elif escolha == '3':
                listar_remedio(conexao)

            elif escolha == '4':
                listar_tratamentos(conexao)

            elif escolha == '5':
                listar_contatoemergencia(conexao)

            elif escolha == '6':
                continue
            else:
                print('Opção inválida.')

        # =========================
        # ADICIONAR
        # =========================
        elif opcao == '2':

            print('\n===== ADICIONAR =====')
            print('1 - Usuários')
            print('2 - Usuário em Tratamento')
            print('3 - Remédios')
            print('4 - Tratamentos')
            print('5 - Contatos de Emergência')
            print('6 - Voltar para o menu principal')

            escolha = input('\nEscolha uma opção: ')

            if escolha == '1':
                adicionar_usuario(conexao)

            elif escolha == '2':
                adicionar_usuario_tratamento(conexao)

            elif escolha == '3':
                adicionar_remedio(conexao)

            elif escolha == '4':
                adicionar_tratamento(conexao)

            elif escolha == '5':
                adicionar_contatoemergencia(conexao)

            elif escolha == '6':
                continue

            else:
                print('Opção inválida.')

        # =========================
        # ATUALIZAR
        # =========================
        elif opcao == '3':

            print('\n===== ATUALIZAR =====')
            print('1 - Usuários')
            print('2 - Remédios')
            print('3 - Tratamentos')
            print('4 - Contatos de Emergência')
            print('5 - Voltar para o menu principal')
            escolha = input('\nEscolha uma opção: ')

            if escolha == '1':
                atualizar_usuario(conexao)

            elif escolha == '2':
                atualizar_remedio(conexao)

            elif escolha == '3':
                atualizar_tratamento(conexao)

            elif escolha == '4':
                atualizar_contatoemergencia(conexao)

            elif escolha == '5':
                continue

            else:
                print('Opção inválida.')

        # =========================
        # EXCLUIR
        # =========================
        elif opcao == '4':

            print('\n===== EXCLUIR =====')
            print('1 - Usuários')
            print('2 - Remédios')
            print('3 - Tratamentos')
            print('4 - Contatos de Emergência')
            print('5 - Voltar para o menu principal')
            escolha = input('\nEscolha uma opção: ')

            if escolha == '1':
                print(
                    "Não é possivel excluir usuários, pois é guardado os dados de cadastro para fins de histórico e segurança")

            elif escolha == '2':
                excluir_remedio(conexao)

            elif escolha == '3':
                excluir_tratamento(conexao)

            elif escolha == '4':
                excluir_contatoemergencia(conexao)

            elif escolha == '5':
                continue

            else:
                print('Opção inválida.')

        # =========================
        # SAIR
        # =========================
        elif opcao == '5':
            print("Encerrando sistema...")
            fechar_conexao(conexao)
            break

        else:
            print("Opção inválida.")

        input('\nPressione ENTER para continuar...')

except Exception as e:
    print(f"Erro inesperado: {e}")
    fechar_conexao(conexao)
