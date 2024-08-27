import numpy as np
import pygame
from aps1.objetos import *
from aps1.contas import *
from aps1.assets import *
import os
import pygame.mixer as mixer
from pathlib import Path

def main():
    # inicializando o pygame 
    pygame.init()

    # determinando a primeira tela do jogo
    estado_tela = "inicio"

    # Obtendo o diretório atual onde o script está localizado
    current_dir = Path(os.path.abspath(__file__))

    # Caminho para os arquivos de recursos
    music_path = os.path.join(current_dir, '/assets/musica_jogo/Flashing Lights by Kanye West 64bit version.mp3')
    explosion_sound_path = os.path.join(current_dir, '/assets/images/Som/270310__littlerobotsoundfactory__explosion_04.wav')
    laser_sound_path = os.path.join(current_dir, '/assets/images/Som/348163__djfroyd__laser-one-shot-2.wav')
    background_image_path = os.path.join(current_dir, '/assets/images/backgroung.png')
    menu_branco_path = os.path.join(current_dir, '/assets/images/Menu_branco.png')
    menu_vermelho_path = os.path.join(current_dir, '/assets/images/Menu_vermelho.png')
    menu_fim_path = os.path.join(current_dir, '/assets/images/Fim.png')
    estilingue_image_path = os.path.join(current_dir, '/assets/images/estilingue/estilingue.png')
    angrybirds_image_path = os.path.join(current_dir, '/assets/images/angrybird/angrybird.png')
    meteoro_01_image_path = os.path.join(current_dir, '/assets/images/meteoro/meteoro_01.png')
    meteoro_02_image_path = os.path.join(current_dir, '/assets/images/meteoro/meteoro_02.png')

    planeta_1_images_path = os.path.join(current_dir, '/assets/images/planeta_1/ezgif-7-60b5815381-png-100x100-sprite-png')
    planeta_2_images_path = os.path.join(current_dir, '/assets/images/planeta_2/ezgif-7-6538be690e-png-100x100-sprite-png')
    estrelas_images_path = os.path.join(current_dir, '/assets/images/estrela/ezgif-5-2fd69d133b-png-140x140-sprite-png')

    # importando a musica de fundo do jogo
    pygame.mixer.music.load(music_path)

    # tocando a musica de background do jogo indeterminadamente
    pygame.mixer.music.play(-1)

    # importando os efeitos sonoros do jogo 
    meteoro_explosao_som = pygame.mixer.Sound(explosion_sound_path)
    laser_tiro = pygame.mixer.Sound(laser_sound_path)

    # background do jogo 
    background_image = pygame.image.load(background_image_path)

    # telas de menu e fim do jogo
    tela_menu_branco = pygame.image.load(menu_branco_path)
    tela_menu_vermelho = pygame.image.load(menu_vermelho_path)
    tela_menu_fim = pygame.image.load(menu_fim_path)

    # configuração do tamanho da tela do jogo
    screen = pygame.display.set_mode((1200, 800))

    # configuração do fps do jogo
    clock = pygame.time.Clock()
    FPS = 60

    # imagem estilingue 
    estilingue_imagem = pygame.image.load(estilingue_image_path).convert_alpha()
    estilingue_imagem = pygame.transform.scale(estilingue_imagem, (130, 130))

    # imagem angrybirds
    angrybirds = pygame.image.load(angrybirds_image_path).convert_alpha()
    angrybirds = pygame.transform.scale(angrybirds, (50, 50))  # Ajuste o tamanho conforme necessário

    # imagens meteoros 
    meteoro_01_image = pygame.image.load(meteoro_01_image_path)
    meteoro_02_image = pygame.image.load(meteoro_02_image_path)

    # imagens do planeta 1
    planeta_1_imagens = load_images(planeta_1_images_path, 109)
    current_image_planeta_1 = 0

    # imagens do planeta 2
    planeta_2_imagens = load_images(planeta_2_images_path, 109)
    current_image_planeta_2 = 0

    # imagens estrela
    estrelas_imagens = load_images(estrelas_images_path, 109)
    current_image_estrela = 0

    # loop principal que roda o jogo
    running = True

    while running:

        # tempo em segundos que demora pra rodar uma vez o loop
        tempo = clock.tick(FPS) / 1000

        # posicao do mouse 
        mouse_pos = pygame.mouse.get_pos()

        # tela de incio do jogo
        if estado_tela == "inicio":

            # deixar o botão jogar em vermelho caso o mouse do usuario chegue perto
            if mouse_pos[0] > 400 and mouse_pos[0] < 850 and mouse_pos[1] > 500 and mouse_pos[1] < 750:
                screen.blit(tela_menu_vermelho, (0, 0))
            else:
                screen.blit(tela_menu_branco, (0, 0))

            pygame.display.update()

            for event in pygame.event.get():
                # sair do jogo caso a tela seja fechada 
                if event.type == pygame.QUIT:
                    running = False
                
                # ir para a primeira fase caso o usuario clique no botão jogar
                elif event.type == pygame.MOUSEBUTTONDOWN and mouse_pos[0] > 400 and mouse_pos[0] < 850 and mouse_pos[1] > 500 and mouse_pos[1] < 750:
                    estado_tela = "fase_01"

        # tela da primeira fase do jogo
        elif estado_tela == "fase_01":

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                # caso ocorra um clique, que seria o tiro
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    laser_tiro.play()  # tocar o som de tiro
                    # se a bola não estiver ativa (ainda nao ocorreu o disparo), calcular sua força e sua direção 
                    if not bola['ativa']:
                        movimentacao_bola_argumentos(mouse_pos, estilingue, bola)

            # se a bola estiver ativa, calcular mudanca de posição e velocidade na tela 
            if bola['ativa']:
                movimentacao_bola(bola, tempo, planeta, meteoro_01_hitbox, meteoro_04_hitbox, "1", planeta_2, estrela)
    
            # colocando o background 
            screen.blit(background_image, (0, 0))

            # calcula a distância e direção do mouse em relação ao ponto de origem do estilingue 
            origem = estilingue['posicao']
            direcao = mouse_pos - origem
            distancia = np.linalg.norm(direcao)
            # se a distancia for maior que 200 a linha para e nao tem mais como auemntar a força do tiro
            if distancia > 200:
                direcao_normalizada = direcao / distancia
                ponto_final = origem + direcao_normalizada * 200  # manter a distancia em 200 sempre
            else:
                ponto_final = mouse_pos
            # desenhando a linha
            pygame.draw.line(screen, (255, 0, 0), origem, ponto_final, 2)

            # desenha bola se estiver ativa (usando a imagem do Angry Bird)
            if bola['ativa']:
                angrybird_rect = angrybirds.get_rect(center=bola['posicao'].astype(int))
                screen.blit(angrybirds, angrybird_rect)

            # movendo o estilingue de acordo com a movimentacao do mouse a partir da funcao argumento
            angulo_rotacao_estilingue = Argumento(mouse_pos, estilingue['posicao'])
            rotacao_estilingue = pygame.transform.rotate(estilingue_imagem, angulo_rotacao_estilingue)
            estilingue_rect = rotacao_estilingue.get_rect(center=estilingue['posicao'])
            # desenhando o estilingue 
            screen.blit(rotacao_estilingue, estilingue_rect)

            # desenhando o meteoro_01 e a hitbox
            if meteoro_01_hitbox['ativo']:
                pygame.draw.circle(screen, meteoro_01_hitbox['cor'], meteoro_01_hitbox['posicao'].astype(int), meteoro_01_hitbox['raio'])
                screen.blit(meteoro_01_image, (meteoro_01_hitbox['posicao'][0] - 50, meteoro_01_hitbox['posicao'][1] - 50))

            pygame.display.flip()

            # para ir para a fase 02 
            if meteoro_01_hitbox['ativo'] == False:
                meteoro_explosao_som.play()
                estado_tela = "fase_02"

        # tela da segunda fase do jogo
        elif estado_tela == "fase_02":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    laser_tiro.play()
                    if not bola['ativa']:
                        movimentacao_bola_argumentos(mouse_pos, estilingue, bola)

            if bola['ativa']:
                movimentacao_bola(bola, tempo, planeta, meteoro_02_hitbox, meteoro_04_hitbox, "2", planeta_2, estrela)

            screen.blit(background_image, (0, 0))

            origem = estilingue['posicao']
            direcao = mouse_pos - origem
            distancia = np.linalg.norm(direcao)
            if distancia > 200:
                direcao_normalizada = direcao / distancia
                ponto_final = origem + direcao_normalizada * 200
            else:
                ponto_final = mouse_pos
            pygame.draw.line(screen, (255, 0, 0), origem, ponto_final, 2)

            if bola['ativa']:
                angrybird_rect = angrybirds.get_rect(center=bola['posicao'].astype(int))
                screen.blit(angrybirds, angrybird_rect)

            angulo_rotacao_estilingue = Argumento(mouse_pos, estilingue['posicao'])
            rotacao_estilingue = pygame.transform.rotate(estilingue_imagem, angulo_rotacao_estilingue)
            estilingue_rect = rotacao_estilingue.get_rect(center=estilingue['posicao'])
            screen.blit(rotacao_estilingue, estilingue_rect)

            if meteoro_02_hitbox['ativo']:
                pygame.draw.circle(screen, meteoro_02_hitbox['cor'], meteoro_02_hitbox['posicao'].astype(int), meteoro_02_hitbox['raio'])
                screen.blit(meteoro_01_image, (meteoro_02_hitbox['posicao'][0] - 50, meteoro_02_hitbox['posicao'][1] - 50))

            pygame.draw.circle(screen, planeta['cor'], (planeta['posicao'][0], planeta['posicao'][1]), planeta['raio'])
            screen.blit(planeta_1_imagens[current_image_planeta_1], (planeta['posicao'][0] - 50, planeta['posicao'][1] - 50))
            current_image_planeta_1 += 1
            if current_image_planeta_1 >= len(planeta_1_imagens):
                current_image_planeta_1 = 0

            pygame.display.flip()

            if meteoro_02_hitbox['ativo'] == False:
                meteoro_explosao_som.play()
                estado_tela = "fase_03"

        # tela da terceira fase do jogo
        elif estado_tela == "fase_03":

            planeta['posicao'] = (600, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    laser_tiro.play()
                    if not bola['ativa']:
                        movimentacao_bola_argumentos(mouse_pos, estilingue, bola)

            if bola['ativa']:
                movimentacao_bola(bola, tempo, planeta, meteoro_03_hitbox, meteoro_04_hitbox, "3", planeta_2, estrela)

            screen.blit(background_image, (0, 0))

            origem = estilingue['posicao']
            direcao = mouse_pos - origem
            distancia = np.linalg.norm(direcao)
            if distancia > 200:
                direcao_normalizada = direcao / distancia
                ponto_final = origem + direcao_normalizada * 200
            else:
                ponto_final = mouse_pos
            pygame.draw.line(screen, (255, 0, 0), origem, ponto_final, 2)

            if bola['ativa']:
                angrybird_rect = angrybirds.get_rect(center=bola['posicao'].astype(int))
                screen.blit(angrybirds, angrybird_rect)

            angulo_rotacao_estilingue = Argumento(mouse_pos, estilingue['posicao'])
            rotacao_estilingue = pygame.transform.rotate(estilingue_imagem, angulo_rotacao_estilingue)
            estilingue_rect = rotacao_estilingue.get_rect(center=estilingue['posicao'])
            screen.blit(rotacao_estilingue, estilingue_rect)

            if meteoro_03_hitbox['ativo']:
                pygame.draw.circle(screen, meteoro_03_hitbox['cor'], meteoro_03_hitbox['posicao'].astype(int), meteoro_03_hitbox['raio'])
                screen.blit(meteoro_01_image, (meteoro_03_hitbox['posicao'][0] - 50, meteoro_03_hitbox['posicao'][1] - 50))

            if meteoro_04_hitbox['ativo']:
                pygame.draw.circle(screen, meteoro_04_hitbox['cor'], meteoro_04_hitbox['posicao'].astype(int), meteoro_04_hitbox['raio'])
                screen.blit(meteoro_02_image, (meteoro_04_hitbox['posicao'][0] - 50, meteoro_04_hitbox['posicao'][1] - 50))

            pygame.draw.circle(screen, planeta['cor'], (planeta['posicao'][0], planeta['posicao'][1]), planeta['raio'])
            screen.blit(planeta_1_imagens[current_image_planeta_1], (planeta['posicao'][0] - 50, planeta['posicao'][1] - 50))
            current_image_planeta_1 += 1
            if current_image_planeta_1 >= len(planeta_1_imagens):
                current_image_planeta_1 = 0

            pygame.draw.circle(screen, planeta_2['cor'], (planeta_2['posicao'][0], planeta_2['posicao'][1]), planeta_2['raio'])
            screen.blit(planeta_2_imagens[current_image_planeta_2], (planeta_2['posicao'][0] - 50, planeta_2['posicao'][1] - 50))
            current_image_planeta_2 += 1
            if current_image_planeta_2 >= len(planeta_2_imagens):
                current_image_planeta_2 = 0

            pygame.display.flip()

            if meteoro_03_hitbox['ativo'] == False:
                if meteoro_03_hitbox['explosao_audio'] == 1:
                    meteoro_explosao_som.play()

            if meteoro_04_hitbox['ativo'] == False:
                if meteoro_04_hitbox['explosao_audio'] == 1:
                    meteoro_explosao_som.play()

            if meteoro_03_hitbox['ativo'] == False and meteoro_04_hitbox['ativo'] == False:
                estado_tela = "fase_04"

        # tela da quarta fase do jogo
        elif estado_tela == "fase_04":

            planeta['posicao'] = (1200/2, 800/2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    laser_tiro.play()
                    if not bola['ativa']:
                        movimentacao_bola_argumentos(mouse_pos, estilingue, bola)

            if bola['ativa']:
                movimentacao_bola(bola, tempo, planeta, meteoro_05_hitbox, meteoro_06_hitbox, "4", estrela, estrela_2)

            screen.blit(background_image, (0, 0))

            origem = estilingue['posicao']
            direcao = mouse_pos - origem
            distancia = np.linalg.norm(direcao)
            if distancia > 200:
                direcao_normalizada = direcao / distancia
                ponto_final = origem + direcao_normalizada * 200
            else:
                ponto_final = mouse_pos
            pygame.draw.line(screen, (255, 0, 0), origem, ponto_final, 2)

            if bola['ativa']:
                angrybird_rect = angrybirds.get_rect(center=bola['posicao'].astype(int))
                screen.blit(angrybirds, angrybird_rect)

            angulo_rotacao_estilingue = Argumento(mouse_pos, estilingue['posicao'])
            rotacao_estilingue = pygame.transform.rotate(estilingue_imagem, angulo_rotacao_estilingue)
            estilingue_rect = rotacao_estilingue.get_rect(center=estilingue['posicao'])
            screen.blit(rotacao_estilingue, estilingue_rect)

            if meteoro_05_hitbox['ativo']:
                pygame.draw.circle(screen, meteoro_05_hitbox['cor'], meteoro_05_hitbox['posicao'].astype(int), meteoro_05_hitbox['raio'])
                screen.blit(meteoro_01_image, (meteoro_05_hitbox['posicao'][0] - 50, meteoro_05_hitbox['posicao'][1] - 50))

            if meteoro_06_hitbox['ativo']:
                pygame.draw.circle(screen, meteoro_06_hitbox['cor'], meteoro_06_hitbox['posicao'].astype(int), meteoro_06_hitbox['raio'])
                screen.blit(meteoro_02_image, (meteoro_06_hitbox['posicao'][0] - 50, meteoro_06_hitbox['posicao'][1] - 50))

            pygame.draw.circle(screen, planeta['cor'], (planeta['posicao'][0], planeta['posicao'][1]), planeta['raio'])
            screen.blit(planeta_1_imagens[current_image_planeta_1], (planeta['posicao'][0] - 50, planeta['posicao'][1] - 50))
            current_image_planeta_1 += 1
            if current_image_planeta_1 >= len(planeta_1_imagens):
                current_image_planeta_1 = 0

            pygame.draw.circle(screen, estrela['cor'], (estrela['posicao'][0], estrela['posicao'][1]), estrela['raio'])
            screen.blit(estrelas_imagens[current_image_estrela], (estrela['posicao'][0] - 71, estrela['posicao'][1] - 71))
            current_image_estrela += 1
            if current_image_estrela >= len(estrelas_imagens):
                current_image_estrela = 0

            pygame.draw.circle(screen, estrela_2['cor'], (estrela_2['posicao'][0], estrela_2['posicao'][1]), estrela_2['raio'])
            screen.blit(estrelas_imagens[current_image_estrela], (estrela_2['posicao'][0] - 71, estrela_2['posicao'][1] - 71))
            current_image_estrela += 1
            if current_image_estrela >= len(estrelas_imagens):
                current_image_estrela = 0

            pygame.display.flip()

            if meteoro_05_hitbox['ativo'] == False:
                if meteoro_05_hitbox['explosao_audio'] == 1:
                    meteoro_explosao_som.play()

            if meteoro_06_hitbox['ativo'] == False:
                if meteoro_06_hitbox['explosao_audio'] == 1:
                    meteoro_explosao_som.play()

            if meteoro_05_hitbox['ativo'] == False and meteoro_06_hitbox['ativo'] == False:
                estado_tela = "final"

        # tela final do jogo
        elif estado_tela == "final":

            screen.blit(tela_menu_fim, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    pygame.quit()


if __name__ == "__main__":
    main()