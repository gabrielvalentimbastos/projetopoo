"""
Módulo responsável pelas classes de representação das figuras geométricas e gerência de dados.

@author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
@version 1.0.0
@since 2026-07-13
"""

import math
import pickle

class Figura:
    """
    Classe abstrata que representa uma figura geométrica básica no sistema de desenho.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    """
    def __init__(self, começo_x, começo_y, cor_borda, cor_preenchimento):
        """
        Construtor da classe Figura.

        @param começo_x: Coordenada X inicial do ponto de partida.
        @param começo_y: Coordenada Y inicial do ponto de partida.
        @param cor_borda: Cor de contorno da figura (padrão hexadecimal ou nome de cor).
        @param cor_preenchimento: Cor interna de preenchimento (string vazia se transparente).
        """
        self.x1 = começo_x
        self.y1 = começo_y
        self.x2 = começo_x
        self.y2 = começo_y 
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def atualizar(self, x, y):
        """
        Atualiza as coordenadas finais (ponto de destino) da figura durante o arrasto do mouse.

        @param x: Nova coordenada X do ponto final.
        @param y: Nova coordenada Y do ponto final.
        @return: None
        """
        self.x2 = x
        self.y2 = y
    
    def incompleta(self):
        """
        Verifica se a figura possui dimensões nulas (ponto inicial idêntico ao final).

        @return: True se a figura estiver incompleta (tamanho zero), False caso contrário.
        """
        return (self.x1, self.y1) == (self.x2, self.y2)
    
    def desenhar(self, canvas, rascunho=False):
        """
        Método abstrato para desenhar a figura no Canvas do Tkinter.

        @param canvas: Objeto Canvas do Tkinter onde o desenho será renderizado.
        @param rascunho: Define se a renderização deve ser feita com linhas tracejadas (visualização temporária).
        @return: None
        """
        pass


class Linha(Figura):
    """
    Representa um segmento de reta bidimensional simples.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    @see Figura
    """
    def desenhar(self, canvas, rascunho=False):
        """
        Renderiza a linha no canvas.

        @param canvas: Objeto Canvas do Tkinter.
        @param rascunho: True para renderização pontilhada temporária.
        @return: None
        """
        dash_padrao = (4,2) if rascunho else None
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, dash=dash_padrao)


class Rabisco(Figura):
    """
    Representa um desenho livre composto por múltiplos pontos conectados de forma sequencial.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    @see Figura
    """
    def __init__(self, começo_x, começo_y, cor_borda, cor_preenchimento):
        """
        Inicializa a estrutura do rabisco com uma lista de pontos conectados.

        @param começo_x: Coordenada X do ponto inicial.
        @param começo_y: Coordenada Y do ponto inicial.
        @param cor_borda: Cor do traçado do pincel.
        @param cor_preenchimento: Cor não aplicada diretamente neste tipo de traço livre.
        """
        super().__init__(começo_x, começo_y, cor_borda, cor_preenchimento)
        self.pontos = [(começo_x, começo_y)]

    def atualizar(self, x, y):
        """
        Adiciona novos pontos na sequência do traçado à medida que o usuário arrasta o cursor.

        @param x: Próxima coordenada X detectada.
        @param y: Próxima coordenada Y detectada.
        @return: None
        """
        self.pontos.append((x, y))

    def incompleta(self):
        """
        Verifica se o rabisco contém pontos suficientes para formar uma reta mínima.

        @return: True se possuir 1 ponto ou menos, False se for um desenho válido.
        """
        return len(self.pontos) <= 1
    
    def desenhar(self, canvas, rascunho=False):
        """
        Renderiza o traçado livre ligando todos os pontos intermediários coletados.

        @param canvas: Objeto Canvas do Tkinter.
        @param rascunho: Define se a renderização utiliza visualização tracejada.
        @return: None
        """
        dash_padrao = (4,2) if rascunho else None
        if len(self.pontos) > 1:
            coords = [coord for ponto in self.pontos for coord in ponto]
            canvas.create_line(coords, fill=self.cor_borda, dash=dash_padrao)    


class Retangulo(Figura):
    """
    Representa uma forma geométrica retangular bidimensional.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    @see Figura
    """
    def desenhar(self, canvas, rascunho=False):
        """
        Renderiza o retângulo com borda e preenchimento especificados.

        @param canvas: Objeto Canvas do Tkinter.
        @param rascunho: Define se o contorno temporário será tracejado.
        @return: None
        """
        dash_padrao = (4, 2) if rascunho else None
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, 
                                outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash_padrao)


class Poligono(Figura):
    """
    Representa um polígono regular dinâmico equilátero circunscrito.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    @see Figura
    """
    def __init__(self, começo_x, começo_y, cor_borda, cor_preenchimento):
        """
        Construtor da classe Polígono regular circunscrito por raio.

        @param começo_x: Coordenada X do ponto central.
        @param começo_y: Coordenada Y do ponto central.
        @param cor_borda: Cor do contorno externo.
        @param cor_preenchimento: Cor do preenchimento de área do polígono.
        """
        super().__init__(começo_x, começo_y, cor_borda, cor_preenchimento)
        self.pontos = [(começo_x, começo_y)]
        self.max_lados = 3
    
    def atualizar(self, x, y):
        """
        Calcula matematicamente o raio e reconstrói as coordenadas de cada vértice.

        @param x: Coordenada X atual do arrasto do mouse.
        @param y: Coordenada Y atual do arrasto do mouse.
        @return: None
        """
        self.x2 = x
        self.y2 = y
        raio = math.sqrt((x - self.x1)**2 + (y - self.y1)**2)
        angulo_inicial = math.atan2(y - self.y1, x - self.x1)
        self.pontos = []
        
        if self.max_lados == 4:
            self.pontos = [
                (self.x1, self.y1 - raio),
                (self.x1 + raio, self.y1),
                (self.x1, self.y1 + raio),
                (self.x1 - raio, self.y1)
            ]
        else:
            for i in range(self.max_lados):
                angulo = angulo_inicial + (2 * math.pi * i / self.max_lados)
                px = self.x1 + raio * math.cos(angulo)
                py = self.y1 + raio * math.sin(angulo)
                self.pontos.append((px, py))

    def incompleta(self):
        """
        Informa se o polígono possui raio de valor equivalente a zero.

        @return: True se a figura está incompleta, False caso contrário.
        """
        return (self.x1, self.y1) == (self.x2, self.y2)

    def desenhar(self, canvas, rascunho=False):
        """
        Renderiza o polígono aplicando suas coordenadas de vértices calculadas.

        @param canvas: Objeto Canvas do Tkinter.
        @param rascunho: Se True, renderiza com borda tracejada.
        @return: None
        """
        dash_padrao = (4, 2) if rascunho else None
        if len(self.pontos) >= 3:
            coordenadas = [coord for ponto in self.pontos for coord in ponto]
            canvas.create_polygon(coordenadas, outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash_padrao)


class Oval(Figura):
    """
    Representa uma elipse bidimensional delimitada pela sua caixa envolvente.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    @see Figura
    """
    def desenhar(self, canvas, rascunho=False):
        """
        Renderiza a elipse no canvas.

        @param canvas: Objeto Canvas do Tkinter.
        @param rascunho: Define se a borda provisória será pontilhada.
        @return: None
        """
        dash_padrao = (4,2) if rascunho else None
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, 
                           outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash_padrao)


class Circulo(Oval):
    """
    Representa uma forma geométrica perfeitamente circular de raio uniforme.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    @see Oval
    """
    def atualizar(self, x, y):
        """
        Ajusta a altura e largura para que permaneçam iguais, garantindo a proporcionalidade circular.

        @param x: Coordenada X do limite de arraste.
        @param y: Coordenada Y do limite de arraste.
        @return: None
        """
        largura = abs(x - self.x1)
        altura = abs(y - self.y1)
        tamanho = max(largura, altura)
        
        self.x2 = self.x1 + tamanho if x >= self.x1 else self.x1 - tamanho
        self.y2 = self.y1 + tamanho if y >= self.y1 else self.y1 - tamanho


class Desenho:
    """
    Classe de modelo responsável pelo armazenamento de dados e persistência física de arquivos.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    """
    def __init__(self):
        """
        Construtor da classe de persistência e gerenciamento do histórico de desenhos.
        """
        self.figuras = []
        self.figura_nova = None

    def adicionar_figura(self, figura):
        """
        Insere de forma definitiva uma nova figura concluída no histórico do desenho.

        @param figura: Instância de uma classe derivada de Figura.
        @return: None
        """
        self.figuras.append(figura)

    def limpar_figura_nova(self):
        """
        Reseta o estado da variável de desenho ativo e temporário do canvas.

        @return: None
        """
        self.figura_nova = None
    
    def salvar_em_arquivo(self, caminho_arquivo):
        """
        Serializa e salva a lista de figuras usando formato binário através da biblioteca pickle.

        @param caminho_arquivo: Caminho completo de destino do arquivo gravado no sistema operacional.
        @return: None
        @throws IOError: Dispara exceção de Input/Output se houver falhas de permissão de escrita física.
        """
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.figuras, arquivo)

    def carregar_de_arquivo(self, caminho_arquivo):
        """
        Carrega um arquivo contendo a lista de objetos geométricos serializados.

        @param caminho_arquivo: Caminho físico de leitura do arquivo.
        @return: None
        @throws IOError: Caso falhe no processo de leitura ou carregamento de dados corrompidos.
        """
        with open(caminho_arquivo, 'rb') as arquivo:
            self.figuras = pickle.load(arquivo)