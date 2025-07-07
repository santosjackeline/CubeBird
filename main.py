import pygame
import random

pygame.init()

# configurações da janela
LARGURA_TELA = 400
ALTURA_TELA = 600
tela_jogo = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Cube Bird")

# carregamento dos recursos
fundo = pygame.image.load("assets/background.png")
sprite_passaro = pygame.image.load("assets/bird.png")
sprite_cano = pygame.image.load("assets/pipe.png")
audio_pulo = pygame.mixer.Sound("assets/som_pulo.wav")

# configurações do jogo
forca_gravidade = 0.8
impulso_pulo = -12
velocidade_lateral = 4
fps = pygame.time.Clock()

# cores utilizadas
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

class Personagem:
    def __init__(self):
        self.pos_x = 100
        self.pos_y = 300
        self.vel_vertical = 0
        self.dimensao_x = sprite_passaro.get_width()
        self.dimensao_y = sprite_passaro.get_height()
        
    def executar_pulo(self):
        self.vel_vertical = impulso_pulo
        audio_pulo.play()
    
    def processar_fisica(self):
        self.vel_vertical += forca_gravidade
        self.pos_y += self.vel_vertical
        
    def renderizar(self):
        tela_jogo.blit(sprite_passaro, (self.pos_x, self.pos_y))
        
    def obter_retangulo(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.dimensao_x, self.dimensao_y)

class EstruturaObstaculo:
    def __init__(self, posicao_inicial):
        self.coordenada_x = posicao_inicial
        self.largura_elemento = sprite_cano.get_width()
        self.altura_elemento = sprite_cano.get_height()
        self.abertura_central = 180
        self.nivel_abertura = random.randint(100, 400)
        self.ja_pontuou = False
        
    def atualizar_posicao(self):
        self.coordenada_x -= velocidade_lateral
        
    def exibir_estrutura(self):
        # parte superior invertida
        elemento_superior = pygame.transform.flip(sprite_cano, False, True)
        tela_jogo.blit(elemento_superior, (self.coordenada_x, self.nivel_abertura - self.altura_elemento))
        
        # parte inferior
        tela_jogo.blit(sprite_cano, (self.coordenada_x, self.nivel_abertura + self.abertura_central))
        
    def verificar_colisao(self, personagem):
        rect_personagem = personagem.obter_retangulo()
        
        # retangulo parte superior
        rect_superior = pygame.Rect(self.coordenada_x, 0, self.largura_elemento, self.nivel_abertura)
        
        # retangulo parte inferior  
        rect_inferior = pygame.Rect(self.coordenada_x, self.nivel_abertura + self.abertura_central, 
                                   self.largura_elemento, ALTURA_TELA)
        
        return rect_personagem.colliderect(rect_superior) or rect_personagem.colliderect(rect_inferior)
    
    def esta_fora_tela(self):
        return self.coordenada_x < -self.largura_elemento
    
    def passou_personagem(self, personagem):
        return self.coordenada_x + self.largura_elemento < personagem.pos_x

def exibir_pontuacao(valor):
    fonte_pontos = pygame.font.Font(None, 50)
    texto_pontos = fonte_pontos.render(str(valor), True, BRANCO)
    tela_jogo.blit(texto_pontos, (LARGURA_TELA // 2 - 15, 50))

def mostrar_menu_inicial():
    tela_jogo.blit(fundo, (0, 0))
    
    fonte_titulo = pygame.font.Font(None, 40)
    fonte_instrucao = pygame.font.Font(None, 25)
    
    titulo_linha1 = fonte_titulo.render("CUBE", True, BRANCO)
    titulo_linha2 = fonte_titulo.render("BIRD", True, BRANCO)
    instrucao = fonte_instrucao.render("Aperte ESPACO para jogar", True, BRANCO)
    
    tela_jogo.blit(titulo_linha1, (LARGURA_TELA // 2 - 40, 200))
    tela_jogo.blit(titulo_linha2, (LARGURA_TELA // 2 - 35, 250))
    tela_jogo.blit(instrucao, (LARGURA_TELA // 2 - 120, 350))
    
    pygame.display.update()

def mostrar_fim_jogo(pontos_obtidos):
    fonte_grande = pygame.font.Font(None, 60)
    fonte_media = pygame.font.Font(None, 30)
    
    sobreposicao = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    sobreposicao.set_alpha(150)
    sobreposicao.fill(PRETO)
    tela_jogo.blit(sobreposicao, (0, 0))
    
    texto_fim = fonte_grande.render("PERDEU!", True, BRANCO)
    texto_resultado = fonte_media.render(f"Fez {pontos_obtidos} pontos", True, BRANCO)
    texto_continuar = fonte_media.render("ESPACO para jogar de novo", True, BRANCO)
    
    tela_jogo.blit(texto_fim, (LARGURA_TELA // 2 - 100, 200))
    tela_jogo.blit(texto_resultado, (LARGURA_TELA // 2 - 80, 300))
    tela_jogo.blit(texto_continuar, (LARGURA_TELA // 2 - 140, 350))
    
    pygame.display.update()

def executar_jogo():
    estado_atual = "menu"
    
    while True:
        if estado_atual == "menu":
            mostrar_menu_inicial()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    # inicializar nova partida
                    estado_atual = "jogando"
                    heroi = Personagem()
                    obstaculos = []
                    contador_pontos = 0
                    cronometro_obstaculo = 0
                    
        elif estado_atual == "jogando":
            fps.tick(60)
            
            # processar entrada
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    heroi.executar_pulo()
            
            # atualizar personagem
            heroi.processar_fisica()
            
            # gerenciar obstáculos
            cronometro_obstaculo += 1
            if cronometro_obstaculo > 90:
                obstaculos.append(EstruturaObstaculo(LARGURA_TELA))
                cronometro_obstaculo = 0
            
            # processar lista de obstáculos
            obstaculos_removidos = []
            for obstaculo in obstaculos:
                obstaculo.atualizar_posicao()
                
                # verificar colisão
                if obstaculo.verificar_colisao(heroi):
                    estado_atual = "fim_jogo"
                    break
                
                # contar pontos
                if not obstaculo.ja_pontuou and obstaculo.passou_personagem(heroi):
                    contador_pontos += 1
                    obstaculo.ja_pontuou = True
                
                # marcar para remoção
                if obstaculo.esta_fora_tela():
                    obstaculos_removidos.append(obstaculo)
            
            # remover obstáculos
            for obstaculo in obstaculos_removidos:
                obstaculos.remove(obstaculo)
            
            # verificar limites da tela
            if heroi.pos_y > ALTURA_TELA - heroi.dimensao_y or heroi.pos_y < 0:
                estado_atual = "fim_jogo"
            
            # renderizar tudo
            if estado_atual == "jogando":
                tela_jogo.blit(fundo, (0, 0))
                
                for obstaculo in obstaculos:
                    obstaculo.exibir_estrutura()
                    
                heroi.renderizar()
                exibir_pontuacao(contador_pontos)
                
                pygame.display.update()
                
        elif estado_atual == "fim_jogo":
            mostrar_fim_jogo(contador_pontos)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    estado_atual = "menu"

if __name__ == "__main__":
    executar_jogo()
