from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y),cor_borda_atual,cor_preenchimento_atual)
    elif tipo_figura_var.get() == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y),cor_borda_atual,cor_preenchimento_atual)
    elif tipo_figura_var.get() == 'Circulo':
        figura_nova = ("circulo", (event.x, event.y, event.x, event.y),cor_borda_atual,cor_preenchimento_atual)
    elif tipo_figura_var.get() == 'Retangulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y),cor_borda_atual,cor_preenchimento_atual)
    else:
        figura_nova = ("rabisco", [(event.x, event.y)],cor_borda_atual,cor_preenchimento_atual)

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
        figura_nova = (figura_nova[0], figura_nova[1], figura_nova[2], figura_nova[3])
    elif figura_nova[0] == "circulo":
        largura = abs(event.x - figura_nova[1][0])
        altura = abs(event.y - figura_nova[1][1])
        tamanho = max(largura, altura)
        x_final = figura_nova[1][0] + tamanho if event.x >= figura_nova[1][0] else figura_nova[1][0] - tamanho
        y_final = figura_nova[1][1] + tamanho if event.y >= figura_nova[1][1] else figura_nova[1][1] - tamanho
        figura_nova = (figura_nova[0], (figura_nova[1][0], figura_nova[1][1], x_final, y_final), figura_nova[2], figura_nova[3])
    else: # figura_nova[0] == 'linha', 'circulo' ou 'retângulo'
        figura_nova = (figura_nova[0], (figura_nova[1][0], figura_nova[1][1], event.x, event.y),figura_nova[2],figura_nova[3])
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
    if not incompleta(figura_nova): 
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values,cor_borda,cor_preenche in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3],fill=cor_borda)
        elif fig == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3],outline=cor_borda,fill=cor_preenche)
        elif fig == "circulo":
            canvas.create_oval(values[0], values[1], values[2], values[3],outline=cor_borda,fill=cor_preenche)
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3],outline=cor_borda,fill=cor_preenche)
        else: # fig == "rabisco"
            canvas.create_line(values,fill=cor_borda)

def desenhar_figura_nova():
    fig, values, cor_borda,cor_preenche = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2),outline=cor_borda,fill=cor_preenche)
    elif fig == "circulo":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2),outline=cor_borda,fill=cor_preenche)
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2),outline=cor_borda,fill=cor_preenche)
    else: # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2))

def incompleta(figura): 
    fig, values,cor_borda,cor_preenche = figura
    if fig in ["linha", "oval", "circulo", "retangulo"]:
        return (values[0], values[1]) == (values[2], values[3])
    else: # fig == "rabisco"
        return len(values) <= 1
def escolher_cor_borda():
    global cor_borda_atual
    cor = colorchooser.askcolor(title='Escolha a cor da borda')[1]
    if cor:
        cor_borda_atual = cor
def escolher_cor_preenchimento():
    global cor_preenchimento_atual
    cor = colorchooser.askcolor(title='Escolha a cor do preenchimento')[1]
    if cor:
        cor_preenchimento_atual = cor

#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
cor_borda_atual = 'black'
cor_preenchimento_atual = ""
root = Tk()
root.title('Exemplo de aplicação com Círculos e Retângulos')
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame, text='Escolha o tipo de desenho:')
label.grid(column=0, row=0, sticky=W, **paddings)

# option menu 
tipo_figura_var = StringVar(root)
option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                              'Linha', 'Linha', 'Rabisco', 'Oval', 'Circulo', 'Retangulo')
option_menu.grid(column=1, row=0, sticky=W, **paddings)
botao_borda = ttk.Button(frame,text='Cor da borda',command=escolher_cor_borda)
botao_borda.grid(column=2,row=0,sticky=W,**paddings)
botao_preenche = ttk.Button(frame,text='Cor de preenchimento',command=escolher_cor_preenchimento)
botao_preenche.grid(column=3,row=0,sticky=W,**paddings)
# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=2, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()