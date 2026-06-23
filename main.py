from tkinter import *


#__________MAIN________#
circulos = []
raio = None

janela = Tk()
janela.title('Paint da shopee')
janela.geometry('1600x800')

canvas = Canvas(janela, bg="white", width=1200, height=800)
canvas.pack()

ini_x = None
ini_y = None
fim_x = None
fim_y = None
#canvas.bind('<ButtonPress-1>',inicia_linha)
#canvas.bind('<B1-Motion>',)
#canvas.bind('<ButtonRelease-1>',)
            
janela.mainloop()
