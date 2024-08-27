import numpy as np

''''
Todas as informaçoes dos objetos salvos em dicionarios 
'''

estilingue = {
    'posicao': np.array([50, 720]),
    'largura': 100
}

bola = {
    'posicao': np.array([0, 0], dtype=np.float64),
    'velocidade': np.array([0, 0], dtype=np.float64),
    'raio': 5,
    'cor': (0, 255, 0),
    'ativa': False
}

meteoro_01_hitbox = {
    'posicao': np.array([1150, 400]),  
    'raio': 25,  
    'cor': (255, 255, 0,0),  
    'ativo': True  
}

planeta = {
    'posicao': np.array([600, 400], dtype=np.float64),
    'raio' : 48,
    'raio_gravidade': 200,
    'cor': (255, 255, 255),
}

planeta_2 = {
    'posicao': np.array([840, 650], dtype=np.float64),
    'raio' : 48,
    'raio_gravidade': 200,
    'cor': (255, 255, 255),
}

estrela = {
    'posicao': np.array([1200/2,800/2-200], dtype=np.float64),
    'raio' : 34,
    'raio_gravidade': 200,
    'cor': (255, 255, 255),
}

estrela_2 = {
    'posicao': np.array([1200/2+500,800/2+200], dtype=np.float64),
    'raio' : 34,
    'raio_gravidade': 200,
    'cor': (255, 255, 255),
}

meteoro_02_hitbox = {
    'posicao': np.array([1150, 600]),  
    'raio': 25,  
    'cor': (255, 255, 0,0),  
    'ativo': True  
}

meteoro_03_hitbox = {
    'posicao': np.array([750, 100]),  
    'raio': 25,  
    'cor': (255, 255, 0,0),  
    'ativo': True ,
    'explosao_audio':0
}

meteoro_04_hitbox = {
    'posicao': np.array([1050, 500]),  
    'raio': 30,  
    'cor': (255, 255, 0,0),  
    'ativo': True ,
    'explosao_audio':0
}

meteoro_05_hitbox = {
    'posicao': np.array([800, 150]),  
    'raio': 25,  
    'cor': (255, 255, 0,0),  
    'ativo': True,
    'explosao_audio':0
}

meteoro_06_hitbox = {
    'posicao': np.array([450, 100]),  
    'raio': 30,  
    'cor': (255, 255, 0,0),  
    'ativo': True,
    'explosao_audio':0
}