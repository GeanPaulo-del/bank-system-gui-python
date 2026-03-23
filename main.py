import tkinter as tk
from tkinter import messagebox
import json

# -------------------------------
# CARREGAR DADOS
# -------------------------------
def carregar_dados():
    try:
        with open("usuarios.json", "r") as arquivo:
            return json.load(arquivo)
    except:
        return {}

# -------------------------------
# SALVAR DADOS
# -------------------------------
def salvar_dados():
    with open("usuarios.json", "w") as arquivo:
        json.dump(usuarios, arquivo)

usuarios = carregar_dados()

# se não existir usuário, cria padrão
if "gean" not in usuarios:
    usuarios["gean"] = {"senha": "123", "saldo": 100}
    salvar_dados()

usuario_logado = None

# -------------------------------
# LOGIN
# -------------------------------
def fazer_login():
    global usuario_logado

    usuario = entrada_usuario.get()
    senha = entrada_senha.get()

    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        usuario_logado = usuario
        abrir_banco()
    else:
        messagebox.showerror("Erro", "Login inválido")

# -------------------------------
# TELA DO BANCO
# -------------------------------
def abrir_banco():
    janela_login.destroy()

    banco = tk.Tk()
    banco.title("Banco")
    banco.geometry("300x250")

    saldo_var = tk.StringVar()

    def atualizar_saldo():
        saldo_var.set(f"Saldo: R$ {usuarios[usuario_logado]['saldo']:.2f}")

    atualizar_saldo()

    tk.Label(banco, textvariable=saldo_var).pack(pady=10)

    # -------------------------------
    # DEPOSITAR
    # -------------------------------
    def depositar():
        try:
            valor = float(entry_valor.get())

            if valor > 0:
                usuarios[usuario_logado]["saldo"] += valor
                salvar_dados()
                atualizar_saldo()
            else:
                messagebox.showerror("Erro", "Valor inválido")

        except:
            messagebox.showerror("Erro", "Digite um número válido")

    # -------------------------------
    # SACAR
    # -------------------------------
    def sacar():
        try:
            valor = float(entry_valor.get())

            if valor <= 0:
                messagebox.showerror("Erro", "Valor inválido")
            elif valor > usuarios[usuario_logado]["saldo"]:
                messagebox.showerror("Erro", "Saldo insuficiente")
            else:
                usuarios[usuario_logado]["saldo"] -= valor
                salvar_dados()
                atualizar_saldo()

        except:
            messagebox.showerror("Erro", "Digite um número válido")

    entry_valor = tk.Entry(banco)
    entry_valor.pack(pady=5)

    tk.Button(banco, text="Depositar", command=depositar).pack(pady=5)
    tk.Button(banco, text="Sacar", command=sacar).pack(pady=5)

    banco.mainloop()

# -------------------------------
# TELA DE LOGIN
# -------------------------------
janela_login = tk.Tk()
janela_login.title("Login")
janela_login.geometry("300x200")

tk.Label(janela_login, text="Usuário").pack()
entrada_usuario = tk.Entry(janela_login)
entrada_usuario.pack()

tk.Label(janela_login, text="Senha").pack()
entrada_senha = tk.Entry(janela_login, show="*")
entrada_senha.pack()

tk.Button(janela_login, text="Login", command=fazer_login).pack(pady=10)

janela_login.mainloop()
