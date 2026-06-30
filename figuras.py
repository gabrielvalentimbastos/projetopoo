class Figura:
    def __init__(self, valores, cor_borda, cor_preenchimento):
        self.valores = valores  # esses valores aq sao as coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    def desenhar(self, canvas):
        pass

    def desenhar_tracejado(self, canvas):
        pass


class Linha(Figura):
    def desenhar(self, canvas):
        canvas.create_line(self.valores[0], self.valores[1], self.valores[2], self.valores[3], fill=self.cor_borda)

    def desenhar_tracejado(self, canvas):
        canvas.create_line(self.valores[0], self.valores[1], self.valores[2], self.valores[3], dash=(4, 2), fill=self.cor_borda)


class Rabisco(Figura):
    def desenhar(self, canvas):
        canvas.create_line(self.valores, fill=self.cor_borda)

    def desenhar_tracejado(self, canvas):
        canvas.create_line(self.valores, dash=(4, 2), fill=self.cor_borda)


class Oval(Figura):
    def desenhar(self, canvas):
        canvas.create_oval(self.valores[0], self.valores[1], self.valores[2], self.valores[3], 
                           outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_tracejado(self, canvas):
        canvas.create_oval(self.valores[0], self.valores[1], self.valores[2], self.valores[3], 
                           dash=(4, 2), outline=self.cor_borda, fill=self.cor_preenchimento)


class Circulo(Oval):
    # o tamanho mexe la na parte do movimento do mouse, de resto é igual ao oval
    pass


class Retangulo(Figura):
    def desenhar(self, canvas):
        canvas.create_rectangle(self.valores[0], self.valores[1], self.valores[2], self.valores[3], 
                                 outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_tracejado(self, canvas):
        canvas.create_rectangle(self.valores[0], self.valores[1], self.valores[2], self.valores[3], 
                                 dash=(4, 2), outline=self.cor_borda, fill=self.cor_preenchimento)


class Poligono(Figura):
    def desenhar(self, canvas):
        # os poligonos usam os valores, tipo oq usamos no rabisco
        if len(self.valores) > 2:
            canvas.create_polygon(self.valores, outline=self.cor_borda, fill=self.cor_preenchimento)

    def desenhar_tracejado(self, canvas):
        if len(self.valores) > 1:
            canvas.create_line(self.valores, dash=(4, 2), fill=self.cor_borda)