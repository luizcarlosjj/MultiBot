from PyQt5 import uic,QtWidgets
import sqlite3



## FUNÇÕES ##
# Login
def user_logado():
    nome_usuario = login.user.text()
    senha = login.passwd.text()
    banco = sqlite3.connect("db/banco_cadastro.db")
    cursor = banco.cursor()
    try:
        cursor.execute("SELECT senha FROM cadastro WHERE nome = '{}'" .format(nome_usuario))
        senha_bd = cursor.fetchall()
        banco.close()
    except:
        print('erro, usuario inválido.')

    if senha == senha_bd[0][0]:
        login.close()
        segunda_tela.show()
        login.label_5.setText("")
    else:
        login.label_5.setText("Dados de login incorretos")

# Cadastrar:
def cadastrar():
    nome= tela_cadastro.user.text()
    idade= tela_cadastro.user_2.text()
    senha= tela_cadastro.user_3.text()
    c_senha= tela_cadastro.user_4.text()

    if (senha == c_senha):
        try:
            banco = sqlite3.connect("db/banco_cadastro.db")
            cursor = banco.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (nome text, idade integer, senha text)")
            cursor.execute("INSERT INTO cadastro VALUES ('"+nome+"','"+idade+"','"+senha+"')")

            banco.commit()
            banco.close()
            tela_cadastro.label.setText("Usuário cadastrado com sucesso!")

        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)
    else:
        tela_cadastro.label.setText("As senhas não são iguais!")

# Candidatos
def criar_candidatos():
    nome_candidato = tela_eleicao.lineEdit.text()
    banco = sqlite3.connect("db/banco_cadastro.db")
    cursor = banco.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS candidatos (nome text)")
    cursor.execute("INSERT INTO candidatos VALUES ('"+nome_candidato+"')")
    banco.commit()
    banco.close()
    a = '{}'.format(nome_candidato) 
    nome_c = a.split()
    tela_eleicao.label_4.setText("Candidato cadastrado!")
    # add combobox:
    tela_eleicao.comboBox.addItems(nome_c)


# Entradas:
def entrar_cadastro():
    tela_cadastro.show()

def entrar_eleicao():
    nomeinc = login.user.text()
    banco = sqlite3.connect("db/banco_cadastro.db")
    cursor = banco.cursor()
    cursor.execute("SELECT idade FROM cadastro WHERE nome = '{}'".format(nomeinc))
    idade_db = cursor.fetchall()

    if idade_db[0][0] < 16:
        segunda_tela.label_3.setText("Permisão Negada, idade insulficiente.")
    else:
        tela_eleicao.show()
        
# fim Entradas


# Saídas
def logout_login():
    segunda_tela.close()
    login.show()

def logout_cadastro():
    tela_cadastro.close()

def logout_eleicao():
    tela_eleicao.close()

def logout_votos():
    tela_votos.close()
#fim Saídas


## EVENTOS ##
def votos():
    nome_u = login.user.text()
    cs = tela_eleicao.comboBox.currentText()
    banco = sqlite3.connect("db/banco_cadastro.db")
    cursor = banco.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS votos (nome_candidato text, eleitor text)")
    cursor.execute("INSERT INTO votos VALUES ('"+cs+"','"+nome_u+"')")
    banco.commit()
    banco.close
    tela_eleicao.label_7.setText("Voto Confirmado!")


def limpar_campos():
    tela_eleicao.lineEdit.setText(" ")
    tela_eleicao.label_4.setText(" ")


def listar_dados():
    tela_votos.show()
    banco = sqlite3.connect("db/banco_cadastro.db")
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM votos")
    dados_lidos = cursor.fetchall()
    tela_votos.tableWidget.setRowCount(len(dados_lidos))
    tela_votos.tableWidget.setColumnCount(2)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 2):
            tela_votos.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    
    banco.close()

def contar_votos():
    banco = sqlite3.connect("db/banco_cadastro.db")
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM votos")
    valores = len(cursor.fetchall())
    tela_votos.label.setText("A Qtd de votos foi de: {}".format(valores))
    banco.commit()
    banco.close



app = QtWidgets.QApplication([])
# PAGES:
login = uic.loadUi("pages/login.ui")
segunda_tela = uic.loadUi("pages/segunda_tela.ui")
tela_cadastro = uic.loadUi("pages/tela_cadastro.ui")
tela_eleicao = uic.loadUi("pages/eleicao.ui")
tela_votos = uic.loadUi("pages/listar_dados.ui")

# LOGIN:
login.login.clicked.connect(user_logado)
login.pushButton_2.clicked.connect(entrar_cadastro)
senha_limite_log = login.passwd.setMaxLength(8)


# Segunda Tela
segunda_tela.pushButton.clicked.connect(logout_login)
segunda_tela.pushButton_2.clicked.connect(entrar_eleicao)

#Tela de Cadastro
tela_cadastro.pushButton.clicked.connect(cadastrar)
tela_cadastro.pushButton_4.clicked.connect(logout_cadastro)
senha_limite_cad = tela_cadastro.user_3.setMaxLength(8)
senha_limite_cad2 = tela_cadastro.user_4.setMaxLength(8)


#Tela de Eleição
tela_eleicao.pushButton.clicked.connect(criar_candidatos)
tela_eleicao.pushButton_2.clicked.connect(limpar_campos)
tela_eleicao.pushButton_3.clicked.connect(votos)
tela_eleicao.pushButton_4.clicked.connect(logout_eleicao)

#Tela Ver Votos
tela_eleicao.pushButton_5.clicked.connect(listar_dados)
tela_votos.pushButton_5.clicked.connect(contar_votos)
tela_votos.pushButton_4.clicked.connect(logout_votos)
 
login.show()
app.exec()