from tkinter import *
from tkinter import ttk

class VisaoDesenho:
    def __init__(self, root):
        self.root = root
        self.root.title('Paint da Shopee')
        self.interface()

    def interface(self):    
        frame = Frame(self.root)
        paddings = {'padx': 5, 'pady': 5} 

        label = ttk.Label(frame, text='Escolha o tipo de desenho:')
        label.grid(column=0, row=0, sticky=W, **paddings)

        # Variáveis do Tkinter (agora acessadas pelo Controlador)
        self.tipo_figura_var = StringVar(self.root)
        self.tipo_figura_var.set('Linha') # Definindo valor inicial
        option_menu = ttk.OptionMenu(frame, self.tipo_figura_var,
                                'Linha', 'Linha', 'Rabisco', 'Oval', 'Circulo', 'Retangulo', 'Poligono')
        option_menu.grid(column=1, row=0, sticky=W, **paddings)
        
        self.lados_poligono_var = StringVar(self.root)
        self.lados_poligono_var.set('Triangulo') # Definindo valor inicial
        self.menu_lados = ttk.OptionMenu(frame, self.lados_poligono_var,
                                         'Triangulo', 'Triangulo', 
                                         'Losango', 'Pentagono', 'Hexagono')
        
        # Os comandos (command) foram removidos dos botões aqui, 
        # pois o Controlador os injeta via 'config' no método vincular_eventos()
        self.botao_borda = ttk.Button(frame, text='Cor da borda')
        self.botao_borda.grid(column=2, row=0, sticky=W, **paddings)
        
        self.botao_preenche = ttk.Button(frame, text='Cor de preenchimento')
        self.botao_preenche.grid(column=2, row=1, sticky=W, **paddings)
        
        # Área de desenho
        self.canvas = Canvas(frame, bg='white', width=1270, height=700)
        self.canvas.grid(column=0, row=2, columnspan=4, sticky=W, **paddings)

        frame.pack()

    def atualizar_canvas(self, modelo):
        #Este método é chamado pelo Controlador sempre que a tela precisa ser redesenhada.
        self.canvas.delete("all")
        
        # Desenha as figuras prontas
        for figura in modelo.figuras:
            figura.desenhar(self.canvas)   
            
        # Desenha o rascunho temporário
        if modelo.figura_nova:
            modelo.figura_nova.desenhar(self.canvas, rascunho=True)