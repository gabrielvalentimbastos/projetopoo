import math
import pickle

class Figura:
    def __init__(self, começo_x, começo_y, cor_borda, cor_preenchimento):
        self.x1 = começo_x
        self.y1 = começo_y
        self.x2 = começo_x
        self.y2 = começo_y 
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def atualizar(self, x, y):
        self.x2 = x
        self.y2 = y
    
    def incompleta(self):
        return (self.x1, self.y1) == (self.x2, self.y2)
    
    def desenhar(self, canvas, rascunho=False):
        pass


class Linha(Figura):
    def desenhar(self, canvas, rascunho=False):
        dash_padrao = (4,2) if rascunho else None
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_borda, dash=dash_padrao)


class Rabisco(Figura):
    def __init__(self, começo_x, começo_y, cor_borda, cor_preenchimento):
        super().__init__(começo_x, começo_y, cor_borda, cor_preenchimento)
        self.pontos = [(começo_x, começo_y)]

    def atualizar(self, x, y):
        self.pontos.append((x, y))

    def incompleta(self):
        return len(self.pontos) <= 1
    
    def desenhar(self, canvas, rascunho=False):
        dash_padrao = (4,2) if rascunho else None
        if len(self.pontos) > 1:
            coords = [coord for ponto in self.pontos for coord in ponto]
            canvas.create_line(coords, fill=self.cor_borda, dash=dash_padrao)    


class Retangulo(Figura):
    def desenhar(self, canvas, rascunho=False):
        dash_padrao = (4, 2) if rascunho else None
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, 
                                outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash_padrao)


class Poligono(Figura):
    def __init__(self, começo_x, começo_y, cor_borda, cor_preenchimento):
        super().__init__(começo_x, começo_y, cor_borda, cor_preenchimento)
        self.pontos = [(começo_x, começo_y)]
        self.max_lados = 3
    
    def atualizar(self, x, y):
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
        return (self.x1, self.y1) == (self.x2, self.y2)

    def desenhar(self, canvas, rascunho=False):
        dash_padrao = (4, 2) if rascunho else None
        if len(self.pontos) >= 3:
            coordenadas = [coord for ponto in self.pontos for coord in ponto]
            canvas.create_polygon(coordenadas, outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash_padrao)


class Oval(Figura):
    def desenhar(self, canvas, rascunho=False):
        dash_padrao = (4,2) if rascunho else None
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, 
                           outline=self.cor_borda, fill=self.cor_preenchimento, dash=dash_padrao)


class Circulo(Oval):
    def atualizar(self, x, y):
        largura = abs(x - self.x1)
        altura = abs(y - self.y1)
        tamanho = max(largura, altura)
        
        self.x2 = self.x1 + tamanho if x >= self.x1 else self.x1 - tamanho
        self.y2 = self.y1 + tamanho if y >= self.y1 else self.y1 - tamanho


class Desenho: # essa parte aqui gerencia os dados das figuras
    def __init__(self):
        self.figuras = []
        self.figura_nova = None

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def limpar_figura_nova(self):
        self.figura_nova = None
    
    def salvar_em_arquivo(self, caminho_arquivo):
        #Salva a lista atual de figuras no computador.
        with open(caminho_arquivo, 'wb') as arquivo:
            pickle.dump(self.figuras, arquivo)

    def carregar_de_arquivo(self, caminho_arquivo):
        #Lê o arquivo e substitui as figuras atuais.
        with open(caminho_arquivo, 'rb') as arquivo:
            self.figuras = pickle.load(arquivo)