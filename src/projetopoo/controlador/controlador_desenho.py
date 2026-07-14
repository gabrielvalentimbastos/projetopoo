"""
Módulo controlador responsável por mediar a interação entre o Modelo de dados e a Interface gráfica.

@author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
@version 1.0.0
@since 2026-07-13
"""

from tkinter import colorchooser

class ControladorDesenho:
    """
    Classe controladora intermediária da arquitetura MVC. Traduz eventos de mouse e botões em manipulações no Modelo.

    @author Gabriel Rocha Valentim Bastos e Luís Roberto Santana Santos
    @version 1.0.0
    """
    def __init__(self, modelo, visao):
        """
        Associa o controlador às instâncias do modelo e da visão, e inicializa as escutas de eventos gráficos.

        @param modelo: Instância ativa do gerenciador de dados de desenho.
        @param visao: Instância correspondente ao layout de exibição na tela.
        """
        self.modelo = modelo
        self.visao = visao
        
        self.cor_borda_atual = 'black'
        self.cor_preenchimento_atual = ""
        
        self.vincular_eventos()

    def vincular_eventos(self):
        """
        Mapeia os eventos do Tkinter (cliques, movimentos, botões) para os métodos correspondentes do controlador.

        @return: None
        """
        self.visao.tipo_figura_var.trace_add("write", self.verificar_exibicao_poligono)
        self.visao.botao_borda.config(command=self.escolher_cor_borda)
        self.visao.botao_preenche.config(command=self.escolher_cor_preenchimento)
        
        self.visao.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.visao.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.visao.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)

        self.visao.botao_salvar.config(command=self.salvar_desenho)
        self.visao.botao_abrir.config(command=self.abrir_desenho)

    def verificar_exibicao_poligono(self, *args):
        """
        Controla dinamicamente a exibição do menu de seleção do número de lados quando o polígono está ativo.

        @return: None
        """
        if self.visao.tipo_figura_var.get() == 'Poligono':
            self.visao.menu_lados.grid(column=1, row=1, sticky='w', padx=5, pady=5)
        else:
            self.visao.menu_lados.grid_forget()

    def escolher_cor_borda(self):
        """
        Abre o seletor de cores nativo para definir a cor da borda das próximas formas.

        @return: None
        """
        cor = colorchooser.askcolor(title='Escolha a cor da borda')[1]
        if os_cor := cor:
            self.cor_borda_atual = os_cor
    
    def escolher_cor_preenchimento(self):
        """
        Abre o seletor de cores nativo para definir a cor de preenchimento interna das próximas formas.

        @return: None
        """
        cor = colorchooser.askcolor(title='Escolha a cor do preenchimento')[1]
        if os_cor := cor:
            self.cor_preenchimento_atual = os_cor

    def iniciar_figura_nova(self, event): 
        """
        Instancia uma nova figura geométrica no modelo dependendo da opção selecionada na interface.

        @param event: Objeto de evento de clique capturado pelo Tkinter contendo coordenadas X e Y.
        @return: None
        """
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
        """
        Atualiza o rascunho temporário do objeto geométrico enquanto o cursor está em movimento.

        @param event: Objeto de evento do movimento de arraste do mouse.
        @return: None
        """
        if self.modelo.figura_nova:
            self.modelo.figura_nova.atualizar(event.x, event.y)
            self.visao.atualizar_canvas(self.modelo)

    def incluir_figura_nova(self, event): 
        """
        Verifica se a forma desenhada é válida e inclui-a permanentemente no histórico de persistência.

        @param event: Objeto de evento que capturou o release do clique do mouse.
        @return: None
        """
        if self.modelo.figura_nova and not self.modelo.figura_nova.incompleta():
            self.modelo.adicionar_figura(self.modelo.figura_nova)
        self.modelo.limpar_figura_nova()
        self.visao.atualizar_canvas(self.modelo)

    def salvar_desenho(self):
        """
        Solicita um arquivo de destino e manda o modelo salvar as figuras persistidas.

        @return: None
        """
        caminho = self.visao.pedir_caminho_salvar()
        if caminho:
            try:
                self.modelo.salvar_em_arquivo(caminho)
                self.visao.mostrar_mensagem("Sucesso", "Seu desenho foi salvo com sucesso!")
            except Exception as erro:
                self.visao.mostrar_erro("Erro ao salvar", f"Não foi possível salvar:\n{erro}")

    def abrir_desenho(self):
        """
        Solicita ao usuário para abrir um desenho serializado e atualiza o Canvas gráfico.

        @return: None
        """
        caminho = self.visao.pedir_caminho_abrir()
        if caminho:
            try:
                self.modelo.carregar_de_arquivo(caminho)
                self.visao.atualizar_canvas(self.modelo) 
                self.visao.mostrar_mensagem("Sucesso", "Desenho carregado com sucesso!")
            except Exception as erro:
                self.visao.mostrar_erro("Erro ao abrir", f"Arquivo inválido:\n{erro}")