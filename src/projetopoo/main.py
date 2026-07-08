from tkinter import Tk
from modelo.figuras import Desenho
from visao.visao_desenho import VisaoDesenho
from controlador.controlador_desenho import ControladorDesenho

if __name__ == "__main__":
    root = Tk()
    modelo = Desenho()
    visao = VisaoDesenho(root)
    controlador = ControladorDesenho(modelo, visao)
    root.mainloop()