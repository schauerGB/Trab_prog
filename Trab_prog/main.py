import pygame
from random import choice

# Inicializando o Pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)

# Configurando a tela
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Adivinhação")

# Listas de itens
cores = ['vermelho', 'laranja', 'amarelo', 'verde', 'azul', 'rosa', 'roxo']
comida = ['esparguete', 'macarrão', 'arroz', 'bife', 'fiambre', 'queijo']

# Função para renderizar texto centralizado dentro de uma caixa
def render_text_in_box(text, font, color, box):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=box.center)  
    text_rect.y = box.y + (box.height - text_surface.get_height()) // 2  # Ajusta a posição vertical
    screen.blit(text_surface, text_rect)

# Função para exibir texto com quebra automática de linha
def render_text_wrapped_centered(text, font, color, max_width, start_y):
    words = text.split(', ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + ", "
        # Testa se a linha atual com a nova palavra cabe na largura
        if font.size(test_line)[0] > max_width:
            lines.append(current_line.rstrip(", "))
            current_line = word + ", "
        else:
            current_line = test_line
    lines.append(current_line.rstrip(", "))  # Adiciona a última linha

    y = start_y
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(center=(300, y))  # 300 é a metade da largura da tela
        screen.blit(text_surface, text_rect)
        y += font.get_linesize()  # Move o y para a próxima linha

# Função principal do jogo
def main():
    running = True
    TENTATIVA = 0  # Inicia o contador de tentativas
    escolha_geral = None
    categoria = None
    input_text = ''
    mensagem = ''  # Para mostrar se o jogador acertou ou errou
    font = pygame.font.Font(None, 36)
    max_tentativas = 3  # Limite de tentativas
    game_over = False  # Controle para mostrar a tela de game over

    while running:
        screen.fill(WHITE)

        if not game_over:
            if categoria is None:
                # Mensagem de seleção de categoria
                render_text_in_box("Escolha a categoria: (1) Cores (2) Comida", font, BLACK, pygame.Rect(50, 50, 500, 50))

                # Botões para seleção de categoria 
                button_cores = pygame.Rect(100, 150, 200, 50)
                button_comida = pygame.Rect(300, 150, 200, 50)
                pygame.draw.rect(screen, LIGHT_GRAY if button_cores.collidepoint(pygame.mouse.get_pos()) else BLACK, button_cores, border_radius=10)
                pygame.draw.rect(screen, LIGHT_GRAY if button_comida.collidepoint(pygame.mouse.get_pos()) else BLACK, button_comida, border_radius=10)

                # Texto dos botões 
                render_text_in_box("Cores", font, WHITE, button_cores)
                render_text_in_box("Comida", font, WHITE, button_comida)

                # Botão para sair 
                exit_button = pygame.Rect(250, 220, 100, 50)
                pygame.draw.rect(screen, LIGHT_GRAY if exit_button.collidepoint(pygame.mouse.get_pos()) else BLACK, exit_button, border_radius=10)
                render_text_in_box("Sair", font, WHITE, exit_button)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_cores.collidepoint(event.pos):
                            categoria = 'cores'
                            escolha_geral = choice(cores)
                        elif button_comida.collidepoint(event.pos):
                            categoria = 'comida'
                            escolha_geral = choice(comida)
                        elif exit_button.collidepoint(event.pos):
                            running = False  # Sai do jogo

            else:
                # Exibe as alternativas com numeração
                lista_alternativas = cores if categoria == 'cores' else comida
                alternativas_texto = ", ".join([f"{i + 1}. {item}" for i, item in enumerate(lista_alternativas)])
                render_text_wrapped_centered(alternativas_texto, font, BLACK, 600, 150)

                # Exibe mensagem de instrução de adivinhação 
                render_text_in_box(f"Tente adivinhar a {categoria}: ", font, BLACK, pygame.Rect(50, 100, 500, 50))

                # Caixa de entrada para a tentativa 
                input_box = pygame.Rect(100, 280, 400, 50)
                pygame.draw.rect(screen, LIGHT_GRAY, input_box, border_radius=10)

                # Atualiza a tela antes de renderizar o texto
                render_text_in_box(input_text, font, BLACK, input_box)

                # Exibe mensagem de acerto ou erro logo abaixo da caixa de entrada 
                mensagem_text = font.render(mensagem, True, RED if "errou" in mensagem else GREEN)
                mensagem_rect = mensagem_text.get_rect(center=(300, 340))  
                screen.blit(mensagem_text, mensagem_rect)

                # Eventos para a tentativa de adivinhação
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN and TENTATIVA < max_tentativas:
                        if event.key == pygame.K_RETURN:
                            if input_text.isdigit():  # Verifica se o input é um número
                                numero = int(input_text)  # Converte o input para inteiro
                                if 1 <= numero <= len(lista_alternativas):
                                    if lista_alternativas[numero - 1].lower() == escolha_geral:
                                        mensagem = "Você acertou!"
                                        game_over = True  # Termina o jogo quando acerta
                                    else:
                                        TENTATIVA += 1  # Incrementa as tentativas
                                        if TENTATIVA >= max_tentativas:
                                            mensagem = f"Você errou! A resposta era '{escolha_geral}'."
                                            game_over = True  # Mostra tela de game over após o erro final
                                        else:
                                            mensagem = f"Você errou! Tentativa {TENTATIVA} de {max_tentativas}."
                                else:
                                    mensagem = "Número da alternativa inválido! Tente um número entre 1 e 7."
                            else:
                                mensagem = "Por favor, insira um número válido."
                            input_text = ''  # Limpa o texto após a tentativa
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode

        else:
            # Tela de Game Over 
            render_text_in_box("Game Over", font, RED, pygame.Rect(50, 100, 500, 50))
            render_text_in_box(f"A resposta era: '{escolha_geral}'", font, BLACK, pygame.Rect(50, 150, 500, 50))

            # Botões "Tentar de novo" e "Sair" 
            retry_button = pygame.Rect(100, 250, 200, 50)
            quit_button = pygame.Rect(300, 250, 200, 50)

            pygame.draw.rect(screen, LIGHT_GRAY if retry_button.collidepoint(pygame.mouse.get_pos()) else BLACK, retry_button, border_radius=10)
            pygame.draw.rect(screen, LIGHT_GRAY if quit_button.collidepoint(pygame.mouse.get_pos()) else BLACK, quit_button, border_radius=10)

            render_text_in_box("Tentar de novo", font, WHITE, retry_button)
            render_text_in_box("Sair", font, WHITE, quit_button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        # Reinicia o jogo
                        TENTATIVA = 0  # Reinicializa o número de tentativas
                        categoria = None
                        escolha_geral = None
                        input_text = ''
                        mensagem = ''
                        game_over = False
                    elif quit_button.collidepoint(event.pos):
                        running = False

        # Atualiza a tela
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
