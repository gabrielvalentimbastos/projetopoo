from tkinter import colorchooser

class ControladorDesenho:
    def __init__(self, modelo, visao):
        self.modelo = modelo
        self.visao = visao
        
        self.cor_borda_atual = 'black'
        self.cor_preenchimento_atual = ""
        
        self.vincular_eventos()

    def vincular_eventos(self):
        self.visao.tipo_figura_var.trace_add("write", self.verificar_exibicao_poligono)
        self.visao.botao_borda.config(command=self.escolher_cor_borda)
        self.visao.botao_preenche.config(command=self.escolher_cor_preenchimento)
        
        self.visao.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.visao.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.visao.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)

        self.visao.botao_salvar.config(command=self.salvar_desenho)
        self.visao.botao_abrir.config(command=self.abrir_desenho)

    def verificar_exibicao_poligono(self, *args):
        if self.visao.tipo_figura_var.get() == 'Poligono':
            self.visao.menu_lados.grid(column=1, row=1, sticky='w', padx=5, pady=5)
        else:
            self.visao.menu_lados.grid_forget()

    def escolher_cor_borda(self):
        cor = colorchooser.askcolor(title='Escolha a cor da borda')[1]
        if os_cor := cor:
            self.cor_borda_atual = os_cor
    
    def escolher_cor_preenchimento(self):
        cor = colorchooser.askcolor(title='Escolha a cor do preenchimento')[1]
        if os_cor := cor:
            self.cor_preenchimento_atual = os_cor

    def iniciar_figura_nova(self, event): 
        from modelo.figuras import Linha, Rabisco, Oval, Circulo, Retangulo, Poligono
        x, y = event.x, event.y
        tipo = self.visao.tipo_figura_var.get()

        if tipo == 'Linha':
            self.modelo.figura_nova = Linha(x, y, self.cor_borda_atual, self.cor_preenchimento_atual)
        elif tipo == 'Oval':
            self.modelo.figura_nova = Oval(x, y, self.cor_borda_atual, self.cor_preenchimento_atual)
        elif tipo == 'Circulo':
            self.modelo.figura_nova = Circulo(x, y, self.cor_borda_atual, self.cor_preenchimento_atual)
        elif tipo == 'Retangulo':
            self.modelo.figura_nova = Retangulo(x, y, self.cor_borda_atual, self.cor_preenchimento_atual)
        elif tipo == 'Poligono':
            texto_lados = self.visao.lados_poligono_var.get()
            if 'Triangulo' in texto_lados:
                lados = 3
            elif 'Losango' in texto_lados:
                lados = 4
            elif 'Pentagono' in texto_lados:
                lados = 5
            else:
                lados = 6
            self.modelo.figura_nova = Poligono(x, y, self.cor_borda_atual, self.cor_preenchimento_atual)
            self.modelo.figura_nova.max_lados = lados
        else:
            self.modelo.figura_nova = Rabisco(x, y, self.cor_borda_atual, self.cor_preenchimento_atual)

    def atualizar_figura_nova(self, event):
        if self.modelo.figura_nova:
            self.modelo.figura_nova.atualizar(event.x, event.y)
            self.visao.atualizar_canvas(self.modelo)

    def incluir_figura_nova(self, event): 
        if self.modelo.figura_nova and not self.modelo.figura_nova.incompleta():
            self.modelo.adicionar_figura(self.modelo.figura_nova)
        self.modelo.limpar_figura_nova()
        self.visao.atualizar_canvas(self.modelo)

    def salvar_desenho(self):
        caminho = self.visao.pedir_caminho_salvar()
        if caminho:
            try:
                self.modelo.salvar_em_arquivo(caminho)
                self.visao.mostrar_mensagem("Sucesso", "Seu desenho foi salvo com sucesso!")
            except Exception as erro:
                self.visao.mostrar_erro("Erro ao salvar", f"Não foi possível salvar:\n{erro}")

    def abrir_desenho(self):
        caminho = self.visao.pedir_caminho_abrir()
        if caminho:
            try:
                self.modelo.carregar_de_arquivo(caminho)
                self.visao.atualizar_canvas(self.modelo) 
                self.visao.mostrar_mensagem("Sucesso", "Desenho carregado com sucesso!")
            except Exception as erro:
                self.visao.mostrar_erro("Erro ao abrir", f"Arquivo inválido:\n{erro}")