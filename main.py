from PyQt5 import uic,QtWidgets
import sqlite3
import segno
from rich import print
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import pywhatkit
import wikipedia

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
def entrar_criptografia():
    criptoT.show()
def entrar_tina():
    tela_tina.show()
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
def logout_cripto():
    criptoT.close()
def logout_tina():
    tela_tina.close()
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
def contar_votos():
    banco = sqlite3.connect("db/banco_cadastro.db")
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM votos")
    valores = len(cursor.fetchall())
    tela_votos.label.setText("A Qtd de votos foi de: {}".format(valores))
    banco.commit()
    banco.close
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


## SISTEMA DE CRIPTOGRAFIA:
def cripto(frase):
    tradutor = ""
    for letra in frase:
        if letra in "Aa": 
            tradutor = tradutor + '@'
        elif letra in "Bb":
            tradutor = tradutor + '#'
        elif letra in "Cc":
            tradutor = tradutor + '$'
        elif letra in "Dd":
            tradutor = tradutor + '%'
        elif letra in "Ee":
            tradutor = tradutor + '2'
        elif letra in "Ff":
            tradutor = tradutor + '&'
        elif letra in "Gg":
            tradutor = tradutor + '*'
        elif letra in "Hh":
            tradutor = tradutor + '('
        elif letra in "Ii":
            tradutor = tradutor + ')'
        elif letra in "Jj":
            tradutor = tradutor + '+'
        elif letra in "Kk":
            tradutor = tradutor + '='
        elif letra in "Ll":
            tradutor = tradutor + '4'
        elif letra in "Mm":
            tradutor = tradutor + '6'
        elif letra in "Nn":
            tradutor = tradutor + '9'
        elif letra in "Oo":
            tradutor = tradutor + '8'
        elif letra in "Pp":
            tradutor = tradutor + '!'
        elif letra in "Qq":
            tradutor = tradutor + '?'
        elif letra in "Rr":
            tradutor = tradutor + '^'
        elif letra in "Ss":
            tradutor = tradutor + '~'
        elif letra in "Tt":
            tradutor = tradutor + '<'
        elif letra in "Uu":
            tradutor = tradutor + '>'
        elif letra in "Vv":
            tradutor = tradutor + '-'
        elif letra in "Ww":
            tradutor = tradutor + '1'
        elif letra in "Xx":
            tradutor = tradutor + '3'
        elif letra in "Yy":
            tradutor = tradutor + '5'
        elif letra in "Zz":
            tradutor = tradutor + '7'
        elif letra in " ":
            tradutor = tradutor + '_'
        else: 
            tradutor = tradutor + letra
    return tradutor
def showText():
    name = criptoT.lineEdit_2.text()
    textLine = cripto(criptoT.lineEdit.text())
    QrcodeText = cripto(criptoT.lineEdit.text())
    qrcode_seq = segno.make_sequence(QrcodeText, version=1)
    qrcode_seq.save('src/CodeImages/{}.png' .format(name), scale=6)
    criptoT.resultado.setText(textLine)    
def codeImage():
    ##arquivo = 'images/{}.png'.format(tela.lineEdit.text())
    name = criptoT.lineEdit_2.text()
    criptoT.label_3.setStyleSheet("background-image : url(src/CodeImages/{}.png);".format(name))

# ASSISTENTE VIRTUAL:
audio = sr.Recognizer()
maquina = pyttsx3.init()
def executa_comando():
    try:
        with sr.Microphone() as source:
            tela_tina.label_3.setText('Ouvindo...')
            voz = audio.listen(source) # Lista as entradas de audio
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower() # Converte as entradas de audio para minisiculo
            if 'tina' in comando:
                comando = comando.replace('tina', '') # Troca a entrada 'tina' por nada
                maquina.runAndWait()
    except:
        tela_tina.label_3.setText("OFF")

    return comando
def comando_voz_usuario():
    comando = executa_comando()
    if 'horas' in comando:
        hora = datetime.now().strftime('%H:%M')
        maquina.say('Agora são' + hora)
        maquina.runAndWait()

    elif 'dia' in comando:
        data = datetime.today()
        datatxt = f'{data.day} do {data.month}'
        maquina.say('Hoje é dia ' + datatxt)
        maquina.runAndWait()

    elif 'procure por' in comando:
        procurar = comando.replace('procure por', '')
        wikipedia.set_lang('pt')
        resultado = wikipedia.summary(procurar,2) 
        print(resultado)
        maquina.say(resultado)
        maquina.runAndWait()

    elif 'escutar' in comando:
        musica = comando.replace('escutar', '')
        resultado = pywhatkit.playonyt(musica)
        maquina.say('Tocando Musica')
        maquina.runAndWait()

    elif 'enviar mensagem' in comando:
        msg = pywhatkit.sendwhatmsg_instantly('+5562984824354', 'Olá Mãe Bom dia!', 15, True, 2)
        maquina.say('Mensagem enviada!')
        maquina.runAndWait()
    
    comando_voz_usuario()


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
segunda_tela.pushButton_3.clicked.connect(entrar_criptografia)
segunda_tela.pushButton_4.clicked.connect(entrar_tina)

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

#Tela Criptografia
criptoT = uic.loadUi("pages/cripto/tela01.ui")
criptoT.criptoButton.clicked.connect(showText)
criptoT.qrcodeButton_2.clicked.connect(codeImage)
criptoT.qrcodeButton_3.clicked.connect(logout_cripto)

#Tela Tina
tela_tina = uic.loadUi("pages/tina/tina.ui")
tela_tina.pushButton_2.clicked.connect(executa_comando)
tela_tina.pushButton_3.clicked.connect(logout_tina)

login.show()
app.exec()