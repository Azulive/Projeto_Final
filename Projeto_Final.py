# 1. SITUAÇÃO PROBLEMA: CADASTRO DE CLIENTES EM UM COMÉRCIO DE VAREJO 

# A EMPRESA "XYZ COMÉRCIO" TEM DIFICULDADES EM CONTROLAR O CADASTRO DE SEUS CLIENTES. ATUALMENTE, O ARQUIVO COM OS DADOS 
# DOS CLIENTES ESTÁ DESORGANIZADO, E A EQUIPE DE VENDAS TEM ENCONTRADO DIFICULDADES EM ENCONTRAR INFORMAÇÕES RÁPIDO.
# A EMPRESA PRECISA DE UM SISTEMA QUE PERMITA O CADASTRO DE NOVOS CLIENTES, A CONSULTA DE CLIENTES JÁ CADASTRADOS 
# E A EDIÇÃO OU EXCLUSÃO DE DADOS.
#  
# Solução proposta: Criar um sistema que permita o cadastro de novos clientes com informações como nome, e-mail, telefone e endereço.
# Além disso, o sistema permitirá a consulta, edição e exclusão dos dados dos clientes através de uma interface gráfica simples. 



import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def conectar():
    return sqlite3.connect('clientes_x.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute(''' 
      CREATE TABLE IF NOT EXISTS clientes(
             id INTEGER PRIMARY KEY NOT NULL,
             nome TEXT,
             email TEXT,
             telefone INTEGER,
             endereco TEXT                
        )
    ''')
    conn.commit()
    conn.close()

def inserir_clientes():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    if nome and email and telefone and endereco:
       conn = conectar()
       c = conn.cursor()
       c.execute('INSERT INTO clientes(nome, email, telefone, endereco) VALUES(?, ?, ?, ?)', (nome, email, telefone, endereco))
       conn.commit()
       conn.close()
       messagebox.showinfo('Inseridos', 'Os dados estão no banco de dados') 
       exibir_clientes()
    else:
       messagebox.showerror('Erro', 'Ocorreu um erro, os dados não foram inseridos')

def exibir_clientes():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * from clientes')
    clientes = c.fetchall()
    for cliente in clientes:
        tree.insert("", "end", values=(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4]))
    conn.close()

def apagar_cliente():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        conn = conectar() 
        c = conn.cursor()
        c.execute('DELETE FROM clientes WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Exito', 'DADOS DELETADOS')
        exibir_clientes()
    else:
        messagebox.showerror('Erro', 'Dados não deletados')

def atualizar_dados_clientes():
    selected = tree.selection()
    if selected:
        user_id = tree.item(selected)['values'][0]
        novo_nome = entry_nome.get()
        novo_email = entry_email.get()
        novo_telefone = entry_telefone.get()
        novo_endereco = entry_endereco.get()
        if novo_nome and novo_email and novo_telefone and novo_endereco:
            conn = conectar() 
            c = conn.cursor()
            c.execute('UPDATE clientes SET nome = ?, email = ?, telefone = ?, endereco = ? WHERE id = ?', 
                     (novo_nome, novo_email, novo_telefone, novo_endereco, user_id)) 
            conn.commit()
            conn.close()
            messagebox.showinfo('Exito', 'Dados alterados')
            exibir_clientes()
        else:
            messagebox.showerror('Erro', 'Dados não inseridos')
    else:
        messagebox.showwarning('Atenção', 'O dado não foi selecionado')

janela = tk.Tk()
janela.title('CADASTRO DE USÚARIOS')

label_nome = tk.Label(janela, text='NOME')
label_nome.grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_email = tk.Label(janela, text='E-MAIL')
label_email.grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(janela)
entry_email.grid(row=1, column=1, padx=10, pady=10)

label_telefone = tk.Label(janela, text='TELEFONE')
label_telefone.grid(row=2, column=0, padx=10, pady=10)
entry_telefone = tk.Entry(janela)
entry_telefone.grid(row=2, column=1, padx=10, pady=10)

label_endereco = tk.Label(janela, text='ENDEREÇO')
label_endereco.grid(row=3, column=0, padx=10, pady=10)
entry_endereco = tk.Entry(janela)
entry_endereco.grid(row=3, column=1, padx=10, pady=10)

btn_inserir = tk.Button(janela, text='INSERIR CLIENTE', command=inserir_clientes)
btn_inserir.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

btn_atualizar = tk.Button(janela, text='ATUALIZAR DADOS DO CLIENTE', command=atualizar_dados_clientes)
btn_atualizar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

btn_apagar = tk.Button(janela, text='APAGAR CLIENTE', command=apagar_cliente)
btn_apagar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

columns = ('ID', 'NOME', 'E-MAIL', 'TELEFONE', 'ENDEREÇO')
tree = ttk.Treeview(janela, columns=columns, show='headings')
tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)

criar_tabela()
exibir_clientes()

janela.mainloop()