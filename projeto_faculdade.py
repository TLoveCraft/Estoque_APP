import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from datetime import datetime
from kivy.graphics import Color, Rectangle


class Produto:
    def __init__(self, produto_id, nome, categoria, quantidade, preco):
        self.produto_id = produto_id
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.preco = preco

class Categoria:
    def __init__(self, nome):
        self.nome = nome

class Movimentacao:
    def __init__(self, produto_id, tipo, quantidade, data=None):
        self.produto_id = produto_id
        self.tipo = tipo
        self.quantidade = quantidade
        self.data = data or datetime.now()

class GerenciadorEstoque:
    def __init__(self):
        self.produtos = {}  
        self.categorias = {}  
        self.movimentacoes = []  

    def cadastrar_categoria(self, nome):
        if nome in self.categorias:
            raise ValueError("Categoria já existe.")
        self.categorias[nome] = Categoria(nome)

    def cadastrar_produto(self, produto):
        if produto.produto_id in self.produtos:
            raise ValueError("Produto com este ID já existe.")
        if produto.categoria not in self.categorias:
            raise ValueError("Categoria não encontrada.")
        self.produtos[produto.produto_id] = produto

    def consultar_produto(self, produto_id):
        return self.produtos.get(produto_id, None)

    def listar_produtos(self):
        return list(self.produtos.values())

    def registrar_movimentacao(self, produto_id, tipo, quantidade):
        if produto_id not in self.produtos:
            raise ValueError("Produto não encontrado.")
        produto = self.produtos[produto_id]
        if tipo == 'saida' and produto.quantidade < quantidade:
            raise ValueError("Quantidade insuficiente em estoque.")
        if tipo == 'entrada':
            produto.quantidade += quantidade
        elif tipo == 'saida':
            produto.quantidade -= quantidade
        movimentacao = Movimentacao(produto_id, tipo, quantidade)
        self.movimentacoes.append(movimentacao)

    def relatorio_movimentacoes(self):
        return self.movimentacoes


class EstoqueApp(App):
    def build(self):
        self.estoque = GerenciadorEstoque()
        
      
        main_layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
        
      
        with main_layout.canvas.before:
            Color(0.95, 0.95, 1, 1)  
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
            main_layout.bind(size=self._update_rect, pos=self._update_rect)

       
        categoria_label = Label(text="Cadastrar Categoria:", color=(0, 0.2, 0.6, 1), font_size=18)
        self.categoria_input = TextInput(hint_text="Nome da Categoria", multiline=False)
        cadastrar_categoria_btn = Button(text="Cadastrar Categoria", background_color=(0.2, 0.6, 1, 1))

        cadastrar_categoria_btn.bind(on_press=self.cadastrar_categoria)

       
        produto_label = Label(text="Cadastrar Produto:", color=(0, 0.2, 0.6, 1), font_size=18)
        self.produto_id_input = TextInput(hint_text="ID do Produto", input_filter="int", multiline=False)
        self.produto_nome_input = TextInput(hint_text="Nome do Produto", multiline=False)
        self.produto_categoria_input = TextInput(hint_text="Categoria", multiline=False)
        self.produto_quantidade_input = TextInput(hint_text="Quantidade", input_filter="int", multiline=False)
        self.produto_preco_input = TextInput(hint_text="Preço", input_filter="float", multiline=False)
        cadastrar_produto_btn = Button(text="Cadastrar Produto", background_color=(0.3, 0.7, 0.4, 1))

        cadastrar_produto_btn.bind(on_press=self.cadastrar_produto)

        
        movimentacao_label = Label(text="Registrar Movimentação:", color=(0, 0.2, 0.6, 1), font_size=18)
        self.mov_produto_id_input = TextInput(hint_text="ID do Produto", input_filter="int", multiline=False)
        self.mov_tipo_input = TextInput(hint_text="Tipo (entrada/saida)", multiline=False)
        self.mov_quantidade_input = TextInput(hint_text="Quantidade", input_filter="int", multiline=False)
        registrar_movimentacao_btn = Button(text="Registrar Movimentação", background_color=(1, 0.7, 0.2, 1))

        registrar_movimentacao_btn.bind(on_press=self.registrar_movimentacao)

        
        exportar_produtos_btn = Button(text="Exportar Produtos", background_color=(0.3, 0.8, 1, 1))
        exportar_produtos_btn.bind(on_press=self.exportar_relatorio_produtos)

        exportar_movimentacoes_btn = Button(text="Exportar Movimentações", background_color=(0.3, 0.8, 0.6, 1))
        exportar_movimentacoes_btn.bind(on_press=self.exportar_relatorio_movimentacoes)

        main_layout.add_widget(categoria_label)
        main_layout.add_widget(self.categoria_input)
        main_layout.add_widget(cadastrar_categoria_btn)

        main_layout.add_widget(produto_label)
        main_layout.add_widget(self.produto_id_input)
        main_layout.add_widget(self.produto_nome_input)
        main_layout.add_widget(self.produto_categoria_input)
        main_layout.add_widget(self.produto_quantidade_input)
        main_layout.add_widget(self.produto_preco_input)
        main_layout.add_widget(cadastrar_produto_btn)

        main_layout.add_widget(movimentacao_label)
        main_layout.add_widget(self.mov_produto_id_input)
        main_layout.add_widget(self.mov_tipo_input)
        main_layout.add_widget(self.mov_quantidade_input)
        main_layout.add_widget(registrar_movimentacao_btn)

        main_layout.add_widget(exportar_produtos_btn)
        main_layout.add_widget(exportar_movimentacoes_btn)

        return main_layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def cadastrar_categoria(self, instance):
        nome = self.categoria_input.text
        try:
            self.estoque.cadastrar_categoria(nome)
            print(f"Categoria '{nome}' cadastrada.")
        except ValueError as e:
            print(f"Erro: {str(e)}")

    def cadastrar_produto(self, instance):
        try:
            produto = Produto(
                produto_id=int(self.produto_id_input.text),
                nome=self.produto_nome_input.text,
                categoria=self.produto_categoria_input.text,
                quantidade=int(self.produto_quantidade_input.text),
                preco=float(self.produto_preco_input.text)
            )
            self.estoque.cadastrar_produto(produto)
            print(f"Produto '{produto.nome}' cadastrado.")
        except ValueError as e:
            print(f"Erro: {str(e)}")

    def registrar_movimentacao(self, instance):
        try:
            produto_id = int(self.mov_produto_id_input.text)
            tipo = self.mov_tipo_input.text.lower()
            quantidade = int(self.mov_quantidade_input.text)
            self.estoque.registrar_movimentacao(produto_id, tipo, quantidade)
            print(f"Movimentação '{tipo}' registrada.")
        except ValueError as e:
            print(f"Erro: {str(e)}")

    def exportar_relatorio_produtos(self, instance):
        produtos = self.estoque.listar_produtos()
        if not produtos:
            print("Nenhum produto para exportar.")
            return
        with open('relatorio_produtos.csv', 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['ID', 'Nome', 'Categoria', 'Quantidade', 'Preço'])
            for produto in produtos:
                writer.writerow([produto.produto_id, produto.nome, produto.categoria, produto.quantidade, produto.preco])
        print("Relatório de Produtos exportado.")

    def exportar_relatorio_movimentacoes(self, instance):
        movimentacoes = self.estoque.relatorio_movimentacoes()
        if not movimentacoes:
            print("Nenhuma movimentação para exportar.")
            return
        with open('relatorio_movimentacoes.csv', 'w', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['Produto ID', 'Tipo', 'Quantidade', 'Data'])
            for mov in movimentacoes:
                writer.writerow([mov.produto_id, mov.tipo, mov.quantidade, mov.data.strftime("%Y-%m-%d %H:%M:%S")])
        print("Relatório de Movimentações exportado.")


if __name__ == "__main__":
    EstoqueApp().run()
