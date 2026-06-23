from tkinter import *
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Circulo':
        figura_nova = ("circulo", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Retangulo':
        figura_nova = ("retangulo", (event.x, event.y, event.x, event.y))
    else:
        figura_nova = ("rabisco", [(event.x, event.y)])

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
    else: # figura_nova[0] == 'linha', 'circulo' ou 'retângulo'
        figura_nova = (figura_nova[0], (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
    if not incompleta(figura_nova): 
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3])
        elif fig == "circulo":
            canvas.create_oval(values[0], values[1], values[2], values[3])
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3])
        else: # fig == "rabisco"
            canvas.create_line(values)

def desenhar_figura_nova():
    fig, values = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == "circulo":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2))
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2))
    else: # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2))

def incompleta(figura): 
    fig, values = figura
    if fig in ["linha", "circulo", "retangulo"]:
        return (values[0], values[1]) == (values[2], values[3])
    else: # fig == "rabisco"
        return len(values) <= 1


#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

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
                              'Linha', 'Linha', 'Rabisco', 'Circulo', 'Retangulo')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=2, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()