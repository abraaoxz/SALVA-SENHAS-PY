import os
from cryptography.fernet import Fernet

# Gera uma chave e a salva em um arquivo
def gerar_chave():
    chave = Fernet.generate_key()
    with open("chave.key", "wb") as chave_arquivo:
        chave_arquivo.write(chave)

# Carrega a chave de um arquivo
def carregar_chave():
    return open("chave.key", "rb").read()

# Criptografa uma mensagem
def criptografar_mensagem(mensagem, chave):
    f = Fernet(chave)
    return f.encrypt(mensagem.encode())

# Descriptografa uma mensagem
def descriptografar_mensagem(mensagem, chave):
    f = Fernet(chave)
    return f.decrypt(mensagem).decode()

def salvar_senha(servico, usuario, senha):
    chave = carregar_chave()
    senha_criptografada = criptografar_mensagem(senha, chave)
    with open("senhas.txt", "a") as arquivo:
        arquivo.write(f"## {servico}\n")
        arquivo.write(f"- Usuário: {usuario}\n")
        arquivo.write(f"- Senha: {senha_criptografada.decode()}\n\n")

def visualizar_senhas():
    chave = carregar_chave()
    if os.path.exists("senhas.txt"):
        with open("senhas.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                if linha.startswith("- Senha: "):
                    senha_criptografada = linha.split(": ")[1].strip()
                    senha = descriptografar_mensagem(senha_criptografada.encode(), chave)
                    print(f"- Senha: {senha}")
                else:
                    print(linha.strip())
    else:
        print("Nenhuma senha salva ainda.")

def main():
    if not os.path.exists("chave.key"):
        gerar_chave()

    print("Organizador de Senhas")
    while True:
        print("1. Adicionar nova senha")
        print("2. Visualizar senhas salvas")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            servico = input("Digite o nome do serviço: ")
            usuario = input(f"Digite o usuário/email para {servico}: ")
            senha = input(f"Digite a senha para {servico}: ")
            salvar_senha(servico, usuario, senha)
            print(f"As informações para {servico} foram salvas com sucesso!\n")
        elif opcao == "2":
            visualizar_senhas()
        elif opcao == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
