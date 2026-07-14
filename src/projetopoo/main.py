"""
Módulo inicializador da aplicação do Paint da Shopee.

@author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
@version 1.0.0
@since 2026-07-13
"""

import sys
import os
from tkinter import Tk

# Adiciona o diretório 'src' ao PATH do sistema para aceitar as importações relativas estruturadas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelo.figuras import Desenho
from visao.visao_desenho import VisaoDesenho
from controlador.controlador_desenho import ControladorDesenho

def main():
    """
    Função principal que inicializa o loop de execução do Tkinter.
    """
    root = Tk()
    modelo = Desenho()
    visao = VisaoDesenho(root)
    controlador = ControladorDesenho(modelo, visao)
    root.mainloop()

if __name__ == "__main__":
    main()