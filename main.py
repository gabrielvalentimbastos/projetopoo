from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from figuras import Linha, Rabisco, Oval, Circulo, Retangulo, Poligono

#******* MAIN *******#
class AppDesenho():
    def __init__(self,root):
        self.figuras = []       # Todas as figuras desenhadas
        self.figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
        self.cor_borda_atual = 'black'
        self.cor_preenchimento_atual = ""
        self.root = root
        self.root.title('Paint')
        self.interface()

    def interface(self):    
        
        frame = Frame(root)

        # Widgets arranjados com Layout grid dentro de frame
        paddings = {'padx': 5, 'pady': 5} 

        # label
        label = ttk.Label(frame, text='Escolha o tipo de desenho:')
        label.grid(column=0, row=0, sticky=W, **paddings)

        # option menu 
        self.tipo_figura_var = StringVar(self.root)
        option_menu = ttk.OptionMenu(frame, self.tipo_figura_var,
                                'Linha', 'Linha', 'Rabisco', 'Oval', 'Circulo', 'Retangulo', 'Poligono')
        option_menu.grid(column=1, row=0, sticky=W, **paddings)
        botao_borda = ttk.Button(frame,text='Cor da borda',command=self.escolher_cor_borda)
        botao_borda.grid(column=2,row=0,sticky=W,**paddings)
        botao_preenche = ttk.Button(frame,text='Cor de preenchimento',command=self.escolher_cor_preenchimento)
        botao_preenche.grid(column=2,row=1,sticky=W,**paddings)
        # Área de desenho
        self.canvas = Canvas(frame, bg='white', width=1270, height=700)
        self.canvas.grid(column=0, row=2, columnspan=4, sticky=W, **paddings)

        frame.pack()

        # Eventos de mouse associados ao canvas - com seus callbacks
        self.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)

    def iniciar_figura_nova(self, event): 

        if self.tipo_figura_var.get() == 'Linha':
            figura_nova = Linha((event.x, event.y, event.x, event.y),self.cor_borda_atual,self.cor_preenchimento_atual)
        elif self.tipo_figura_var.get() == 'Oval':
            figura_nova = Oval((event.x, event.y, event.x, event.y),self.cor_borda_atual,self.cor_preenchimento_atual)
        elif self.tipo_figura_var.get() == 'Circulo':
            figura_nova = Circulo((event.x, event.y, event.x, event.y),self.cor_borda_atual,self.cor_preenchimento_atual)
        elif self.tipo_figura_var.get() == 'Retangulo':
            figura_nova = Retangulo((event.x, event.y, event.x, event.y),self.cor_borda_atual,self.cor_preenchimento_atual)
        elif self.tipo_figura_var.get() == 'Poligono':
            figura_nova = Poligono([(event.x, event.y)],self.cor_borda_atual, self.cor_preenchimento_atual)
        else:
            figura_nova = Rabisco([(event.x, event.y)],self.cor_borda_atual,self.cor_preenchimento_atual)

    # Quando mouse é movido com o botão pressionado
    def atualizar_figura_nova(self,event):
        if self.figura_nova:
            self.figura_nova.atualizar(event.x, event.y)
            self.desenhar_figuras()
            self.figura_nova.desenhar(self.canvas, rascunho=True)

    # Quando mouse é solto
    def incluir_figura_nova(self,event): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        if self.figura_nova and not self.figura_nova.incompleta():
            self.figuras.append(self.figura_nova)
        self.figura_nova = None
        self.desenhar_figuras()

    def desenhar_figuras(self):
        self.canvas.delete("all")
        for figura in self.figuras:
            figura.desenhar(self.canvas)   

    def escolher_cor_borda(self):
        cor = colorchooser.askcolor(title='Escolha a cor da borda')[1]
        if cor:
            self.cor_borda_atual = cor
    
    def escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor(title='Escolha a cor do preenchimento')[1]
        if cor:
            self.cor_preenchimento_atual = cor

if __name__ == "__main__":
    root = Tk()
    app = AppDesenho(root)
    root.mainloop()