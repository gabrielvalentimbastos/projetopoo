"""
Módulo contendo a implementação da camada de apresentação gráfica da aplicação.

@author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
@version 1.0.0
@since 2026-07-13
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

class VisaoDesenho:
    """
    Classe responsável pela construção da tela gráfica (widgets, botões, seletor de polígonos e menus).

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    """
    def __init__(self, root):
        """
        Inicializa a visão e prepara o container gráfico da interface gráfica do Tkinter.

        @param root: Instância ativa principal da biblioteca Tkinter (Tk).
        """
        self.root = root
        self.root.title('Paint da Shopee')
        self.interface()

    def interface(self):    
        """
        Gera os componentes de layout visuais usando o geometry manager Grid e os insere na janela.

        @return: None
        """
        frame = Frame(self.root)
        paddings = {'padx': 5, 'pady': 5} 

        label = ttk.Label(frame, text='Escolha o tipo de desenho:')
        label.grid(column=0, row=0, sticky=W, **paddings)

        self.tipo_figura_var = StringVar(self.root)
        self.tipo_figura_var.set('Linha')
        option_menu = ttk.OptionMenu(frame, self.tipo_figura_var,
                                'Linha', 'Linha', 'Rabisco', 'Oval', 'Circulo', 'Retangulo', 'Poligono')
        option_menu.grid(column=1, row=0, sticky=W, **paddings)
        
        self.lados_poligono_var = StringVar(self.root)
        self.lados_poligono_var.set('Triangulo')
        self.menu_lados = ttk.OptionMenu(frame, self.lados_poligono_var,
                                         'Triangulo', 'Triangulo', 
                                         'Losango', 'Pentagono', 'Hexagono')
        
        self.botao_borda = ttk.Button(frame, text='Cor da borda')
        self.botao_borda.grid(column=2, row=0, sticky=W, **paddings)
        
        self.botao_preenche = ttk.Button(frame, text='Cor de preenchimento')
        self.botao_preenche.grid(column=2, row=1, sticky=W, **paddings)
        
        self.botao_salvar = ttk.Button(frame, text='Salvar Desenho')
        self.botao_salvar.grid(column=3, row=0, sticky=W, **paddings)

        self.botao_abrir = ttk.Button(frame, text='Abrir Desenho')
        self.botao_abrir.grid(column=3, row=1, sticky=W, **paddings)

        self.canvas = Canvas(frame, bg='white', width=1270, height=700)
        self.canvas.grid(column=0, row=2, columnspan=4, sticky=W, **paddings)

        frame.pack()

    def atualizar_canvas(self, modelo):
        """
        Limpa o canvas completamente e redesenha todas as figuras geométricas armazenadas.

        @param modelo: Instância do modelo que possui o histórico de objetos a serem renderizados.
        @return: None
        """
        self.canvas.delete("all")
        
        for figura in modelo.figuras:
            figura.desenhar(self.canvas)   
            
        if modelo.figura_nova:
            modelo.figura_nova.desenhar(self.canvas, rascunho=True)
    
    def pedir_caminho_salvar(self):
        """
        Exibe ao usuário um seletor nativo do sistema perguntando onde deseja salvar o arquivo de desenho (.pnt).

        @return: Caminho do destino selecionado ou string vazia caso a operação seja cancelada.
        """
        return filedialog.asksaveasfilename(
            title="Salvar Desenho",
            defaultextension=".pnt",
            filetypes=[("Paint da Shopee", "*.pnt"), ("Todos os Arquivos", "*.*")]
        )

    def pedir_caminho_abrir(self):
        """
        Exibe ao usuário um seletor nativo do sistema operacional perguntando qual arquivo carregar (.pnt).

        @return: Caminho do arquivo selecionado para abertura ou string vazia caso a operação seja cancelada.
        """
        return filedialog.askopenfilename(
            title="Abrir Desenho",
            defaultextension=".pnt",
            filetypes=[("Paint da Shopee", "*.pnt"), ("Todos os Arquivos", "*.*")]
        )

    def mostrar_mensagem(self, titulo, mensagem):
        """
        Mostra um pop-up clássico de notificação de sucesso ou informativo na tela do sistema operacional.

        @param titulo: Título exibido no topo da janela pop-up.
        @param mensagem: Descrição textual da notificação informativa.
        @return: None
        """
        messagebox.showinfo(titulo, mensagem)

    def mostrar_erro(self, titulo, mensagem):
        """
        Exibe uma caixa de erro nativa do sistema alertando falhas de gravação ou leitura.

        @param titulo: Título da janela popup de erro.
        @param mensagem: Descrição detalhada sobre o erro técnico acontecido.
        @return: None
        """
        messagebox.showerror(titulo, mensagem)