import math
import numpy as np
import pygame 
import os 

def Argumento(pos_mouse, pos_rect):
    '''
    Calcula o angulo entre o mouse e um ponto da tela (dentro da estilingue) para definir a direçao do disparo
    '''
    x = pos_mouse[0] - pos_rect[0] #diferença no eixo X do mouse e o ponto de referencia
    y = pos_mouse[1] - pos_rect[1] #diferença no eixo Y do mouse e o ponto de referencia
    angle = math.atan2(-y, x) #calcula o angulo em radianos entre esses dois pontos, com y negativado pois ele cresçe para baixo no plano cartesiano do pygame
    return math.degrees(angle) #mudando o angulo para graus 

def caulcula_constante_gravidade(raio_planeta):
    ''''
    dado a formula para calculo de força gravitacional, Fg = (m*M*G)/d**2,
    podemos considerar (m*M*G) como constante,
    para tanto, vamos considerar as o (raio do planeta * uma constante x) para determinar essa constante gravitacional para cada planeta 
    '''
    return raio_planeta * 10**6

def calcular_gravidade_planeta(bola, planeta, constante_gravidade):

    vetor_distancia = bola['posicao'] - planeta['posicao'] #distancia entre a bola e o planeta
    distancia = np.linalg.norm(vetor_distancia) #calcula a distancia escalar entre os dois objetos
    direcao = vetor_distancia / distancia #calcula apenas a direção do vetor, desconsiderando sua magnetude 
    
    gravidade = constante_gravidade / distancia**2 #calcula a força gravitacional a partir da simplificação da formula Fg = (m*M*G)/d**2
    
    return -direcao * gravidade  # retornando o vetor da força gravitacional

def calcular_gravidade_estrela(bola, planeta, constante_gravidade):

    vetor_distancia = bola['posicao'] - planeta['posicao'] #distancia entre a bola e o planeta
    distancia = np.linalg.norm(vetor_distancia) #calcula a distancia escalar entre os dois objetos
    direcao = vetor_distancia / distancia #calcula apenas a direção do vetor, desconsiderando sua magnetude 
    
    gravidade = constante_gravidade / distancia**2 #calcula a força gravitacional a partir da simplificação da formula Fg = (m*M*G)/d**2
    
    return direcao * gravidade  # retornando o vetor da força gravitacional
    
def calcular_velocidade_inicial(angulo, forca):
    '''
    Dado o angulo theta e a força inicial já calculadas, podemos decompor a força para achar as velocidades em x e y:
    como, sen(angulo) = Fy / F
    temos, Fy = F * sen(angulo)
    como estamos desconsiderando a massa e o tempo, podemos concluir que Vy = Fy
    portanto,
    Fy = F * sen(angulo)
    Fx = F * cos(angulo)
    '''
    velocidade_x = math.cos(angulo) * forca
    velocidade_y = -math.sin(angulo) * forca #y negativado pois ele cresçe para baixo no plano cartesiano do pygame
    return np.array([velocidade_x, velocidade_y]) #retorna a velocidade inicial da bola 

def calcular_colisao(centro_1,centro_2,raio_1,raio_2):
    '''
    Calcula a distancia entre duas circuferencia, demonstrando quando ocorre uma colisão entre ambas 
    '''
    distancia_centros = math.sqrt((centro_2[0] - centro_1[0])**2 + (centro_2[1] - centro_1[1])**2)
    if distancia_centros <= (raio_1 + raio_2):
        return True

#carrega todas as imagens dos planetas e estrelas -feito pelo gpt 
def load_images(folder,frames):
    '''
    Função para trocar de imagem a cada frame para parecer que os planetas ou estrelas estão realmente girando
    '''
    images = []
    for i in range(109): 
        image_path = os.path.join(folder, f'tile{str(i).zfill(3)}.png')
        image = pygame.image.load(image_path)
        images.append(image)
    return images

def movimentacao_bola_argumentos(mouse_pos,estilingue,bola):
    '''
    Calcula a força inicial e direçao da bola após seu disparo
    '''
    #calcula a magnetude do vetor dada a distancia do mouse do canhao
    distancia = np.linalg.norm(mouse_pos - (estilingue['posicao']))
    #calcula o angulo de lançamento dado a funcao Argumento
    angulo = math.radians(Argumento(mouse_pos, estilingue['posicao']))
    #força aplicada a bola dada a distancia anteriormente calculada do mouse 
    if distancia < 200:
        forca = distancia * 1.5
    else:
        forca = 200 * 2.5
    #calcula a velovidade inicial da bola dado a força e a distancia
    bola['velocidade'] = calcular_velocidade_inicial(angulo, forca)
    #calcula a posiçao da bola
    bola['posicao'] = np.array([estilingue['posicao'][0]+10,estilingue['posicao'][1]-10], dtype=np.float64)
    #mostrando que a bola está em movimento
    bola['ativa'] = True

def movimentacao_bola(bola,tempo,planeta,meteoro_hitbox1,meteoro_hitbox2,fase,planeta_2,estrela):
    '''
    Calcula a movimentaçao da bola dada as acoes gravitacionais implicadas a tal e colisoes da bola(disparo) com os meteoros em cada fase 
    '''
    #posiçao da bola é alterada dado o tempo e sua velocidade
    if fase == "1":
        bola['posicao'] += bola['velocidade'] * tempo

        #se a bola sair das dimençoes da tela ela para de estar ativa
        if bola['posicao'][1] > 800 or bola['posicao'][0] < 0 or bola['posicao'][0] > 1200 or bola['posicao'][1] < 0:
            bola['ativa'] = False

        #colisoes com os meteoros - vai apagar os meteoros
        if calcular_colisao(bola['posicao'],meteoro_hitbox1['posicao'],bola['raio'],meteoro_hitbox1['raio']):
            meteoro_hitbox1['ativo'] = False 

        #colisoes com os planetas - vai apagar o tiro
        if calcular_colisao(bola['posicao'],planeta['posicao'],bola['raio'],planeta['raio']):
            bola['ativa'] = False 

    elif fase == "2":
        bola['posicao'] += bola['velocidade'] * tempo

        #se a bola sair das dimençoes da tela ela para de estar ativa
        if bola['posicao'][1] > 800 or bola['posicao'][0] < 0 or bola['posicao'][0] > 1200 or bola['posicao'][1] < 0:
            bola['ativa'] = False  

        #caso a bola entre dentro da circuferencia da gravidade do planeta
        gravidade_planeta_01 = calcular_gravidade_planeta(bola, planeta, caulcula_constante_gravidade(planeta['raio']))
        bola['velocidade'] += gravidade_planeta_01 * tempo

        #colisoes com os meteoros - vai apagar os meteoros
        if calcular_colisao(bola['posicao'],meteoro_hitbox1['posicao'],bola['raio'],meteoro_hitbox1['raio']):
            meteoro_hitbox1['ativo'] = False 

        #colisoes com os planetas - vai apagar o tiro
        if calcular_colisao(bola['posicao'],planeta['posicao'],bola['raio'],planeta['raio']):
            bola['ativa'] = False 
    
    elif fase == "3":
        bola['posicao'] += bola['velocidade'] * tempo

        #se a bola sair das dimençoes da tela ela para de estar ativa
        if bola['posicao'][1] > 800 or bola['posicao'][0] < 0 or bola['posicao'][0] > 1200 or bola['posicao'][1] < 0:
            bola['ativa'] = False  

        #caso a bola entre dentro da circuferencia da gravidade do planeta
        gravidade_planeta_01 = calcular_gravidade_planeta(bola, planeta, caulcula_constante_gravidade(planeta['raio']))
        gravidade_planeta_02 = calcular_gravidade_planeta(bola, planeta_2, caulcula_constante_gravidade(planeta_2['raio']))
        gravidade_total = gravidade_planeta_01 + gravidade_planeta_02
        bola['velocidade'] += gravidade_total * tempo

        #colisoes com os meteoros - vai apagar os meteoros
        if calcular_colisao(bola['posicao'],meteoro_hitbox1['posicao'],bola['raio'],meteoro_hitbox1['raio']):
            meteoro_hitbox1['ativo'] = False 
            meteoro_hitbox1['explosao_audio'] += 1 

        if calcular_colisao(bola['posicao'],meteoro_hitbox2['posicao'],bola['raio'],meteoro_hitbox2['raio']):
            meteoro_hitbox2['ativo'] = False 
            meteoro_hitbox2['explosao_audio'] += 1 

        #colisoes com os planetas - vai apagar o tiro
        if calcular_colisao(bola['posicao'],planeta['posicao'],bola['raio'],planeta['raio']):
            bola['ativa'] = False 

        if calcular_colisao(bola['posicao'],planeta_2['posicao'],bola['raio'],planeta_2['raio']):
            bola['ativa'] = False 

    elif fase == "4":
        bola['posicao'] += bola['velocidade'] * tempo

        #se a bola sair das dimençoes da tela ela para de estar ativa
        if bola['posicao'][1] > 800 or bola['posicao'][0] < 0 or bola['posicao'][0] > 1200 or bola['posicao'][1] < 0:
            bola['ativa'] = False  

        #caso a bola entre dentro da circuferencia da gravidade do planeta
        gravidade_planeta_01 = calcular_gravidade_planeta(bola, planeta, caulcula_constante_gravidade(planeta['raio']))
        gravidade_estrela_01 = calcular_gravidade_estrela(bola, planeta_2, caulcula_constante_gravidade(planeta_2['raio']))
        gravidade_estrela_02 = calcular_gravidade_estrela(bola, estrela, caulcula_constante_gravidade(estrela['raio']))
        gravidade_total = gravidade_planeta_01 + gravidade_estrela_01 + gravidade_estrela_02
        bola['velocidade'] += gravidade_total * tempo

        #colisoes com os meteoros - vai apagar os meteoros
        if calcular_colisao(bola['posicao'],meteoro_hitbox1['posicao'],bola['raio'],meteoro_hitbox1['raio']):
            meteoro_hitbox1['ativo'] = False 
            meteoro_hitbox1['explosao_audio'] += 1 
            
        if calcular_colisao(bola['posicao'],meteoro_hitbox2['posicao'],bola['raio'],meteoro_hitbox2['raio']):
            meteoro_hitbox2['ativo'] = False 
            meteoro_hitbox2['explosao_audio'] += 1 

        #colisoes com os planetas - vai apagar o tiro
        if calcular_colisao(bola['posicao'],planeta['posicao'],bola['raio'],planeta['raio']):
            bola['ativa'] = False 

        if calcular_colisao(bola['posicao'],planeta_2['posicao'],bola['raio'],planeta_2['raio']):
            bola['ativa'] = False 