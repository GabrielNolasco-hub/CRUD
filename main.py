import tkinter as tk
from tkinter import ttk, messagebox


class Produto:
    def __init__(self, id, nome, preco, quantidade):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade

    def toString(self):
        return f"{self.id} - {self.nome} - R${self.preco:.2f} - Qtd: {self.quantidade}"


class ProdutoController:
    def __init__(self):
        self.produtos = []
        self.proximo_id = 1

    def adicionar(self, produto):
        produto.id = self.proximo_id
        self.proximo_id += 1
        self.produtos.append(produto)

    def listar(self):
        return self.produtos

    def atualizar(self, id, produto_atualizado):
        for p in self.produtos:
            if p.id == id:
                p.nome = produto_atualizado.nome
                p.preco = produto_atualizado.preco
                p.quantidade = produto_atualizado.quantidade
                return True
        return False

    def remover(self, id):
        for p in self.produtos:
            if p.id == id:
                self.produtos.remove(p)
                return True
        return False


def parse_price(text):
    s = text.strip()

    if s == "":
        raise ValueError("Preço vazio")

    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")

    return float(s)


def format_price_br(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class ProdutoView:
    def __init__(self, root):
        self.controller = ProdutoController()

        root.title("Cadastro de Produtos")
        root.geometry("600x460")
        root.resizable(False, False)

        tk.Label(root, text="Nome:").grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        self.nome_entry = tk.Entry(root, width=40)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(root, text="Preço:").grid(
            row=1, column=0, padx=10, pady=5, sticky="w")
        self.preco_entry = tk.Entry(root, width=20)
        self.preco_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(root, text="Quantidade:").grid(
            row=2, column=0, padx=10, pady=5, sticky="w")
        self.quantidade_entry = tk.Entry(root, width=10)
        self.quantidade_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Button(root, text="Adicionar", width=12,
                  command=self.adicionar).grid(row=0, column=3, padx=10)
        tk.Button(root, text="Listar", width=12, command=self.listar).grid(
            row=1, column=3, padx=10)
        tk.Button(root, text="Atualizar", width=12,
                  command=self.atualizar).grid(row=2, column=3, padx=10)
        tk.Button(root, text="Remover", width=12, command=self.remover).grid(
            row=3, column=3, padx=10)

        tk.Label(root, text="Pesquisar (nome):").grid(
            row=3, column=0, padx=10, pady=10, sticky="w")

        self.search_entry = tk.Entry(root, width=40)
        self.search_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.filtrar_por_nome)

        columns = ("id", "nome", "preco", "quantidade")
        self.tabela = ttk.Treeview(
            root, columns=columns, show="headings", height=12)
        self.tabela.heading("id", text="ID")
        self.tabela.column("id", width=50, anchor="center")
        self.tabela.heading("nome", text="Nome")
        self.tabela.column("nome", width=280, anchor="w")
        self.tabela.heading("preco", text="Preço")
        self.tabela.column("preco", width=120, anchor="e")
        self.tabela.heading("quantidade", text="Quantidade")
        self.tabela.column("quantidade", width=100, anchor="center")

        self.tabela.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        vsb = ttk.Scrollbar(root, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=vsb.set)
        vsb.grid(row=4, column=4, sticky="ns", pady=10)

        tk.Button(root, text="Limpar campos", width=20, command=self.limpar_campos).grid(
            row=5, column=0, columnspan=4, pady=10
        )

        self.tabela.bind("<ButtonRelease-1>", self.preencher_campos)

    def adicionar(self):
        try:
            nome = self.nome_entry.get().strip()
            preco = parse_price(self.preco_entry.get())
            quantidade = int(self.quantidade_entry.get())

            if nome == "":
                messagebox.showerror("Erro", "O nome não pode ficar vazio.")
                return

            produto = Produto(0, nome, preco, quantidade)
            self.controller.adicionar(produto)

            messagebox.showinfo("Sucesso", "Produto adicionado.")
            self.limpar_campos()
            self.listar()

        except Exception as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

    def listar(self):
        self.tabela.delete(*self.tabela.get_children())

        for p in self.controller.listar():
            self.tabela.insert("", tk.END, values=(
                p.id,
                p.nome,
                format_price_br(p.preco),
                p.quantidade
            ))

    def atualizar(self):
        item = self.tabela.selection()
        if not item:
            messagebox.showwarning("Erro", "Selecione um produto.")
            return

        id = int(self.tabela.item(item, "values")[0])

        try:
            nome = self.nome_entry.get().strip()
            preco = parse_price(self.preco_entry.get())
            quantidade = int(self.quantidade_entry.get())

            produto = Produto(id, nome, preco, quantidade)

            if self.controller.atualizar(id, produto):
                messagebox.showinfo("Sucesso", "Produto atualizado.")
                self.listar()
                self.limpar_campos()

        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover(self):
        item = self.tabela.selection()
        if not item:
            messagebox.showwarning("Erro", "Selecione um produto.")
            return

        id = int(self.tabela.item(item, "values")[0])

        if messagebox.askyesno("Confirmação", "Deseja remover este produto?"):
            if self.controller.remover(id):
                self.listar()
                self.limpar_campos()

    def preencher_campos(self, event):
        item = self.tabela.selection()
        if not item:
            return

        id, nome, preco, quantidade = self.tabela.item(item, "values")

        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)

        self.nome_entry.insert(0, nome)
        self.preco_entry.insert(0, preco)
        self.quantidade_entry.insert(0, quantidade)

    def limpar_campos(self):
        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)

    def filtrar_por_nome(self, event):
        termo = self.search_entry.get().lower()

        self.tabela.delete(*self.tabela.get_children())

        for p in self.controller.listar():
            if termo in p.nome.lower():
                self.tabela.insert("", tk.END, values=(
                    p.id,
                    p.nome,
                    format_price_br(p.preco),
                    p.quantidade
                ))


if __name__ == "__main__":
    root = tk.Tk()
    app = ProdutoView(root)
    root.mainloop()
