import pygame
import classes_jogo
import elementos_tela
import dados_cartas
import game_sprites

# inicializacao da janela pygame
game = game_sprites.GameDrawer()

juiz = classes_jogo.Juiz()

# cria as cartas todas as cartas(decks)
quantidade_cartas = dados_cartas.obter_numero_de_cartas()

player_deck = classes_jogo.Deck(quantidade_cartas, 'player')
npc_deck = classes_jogo.Deck(quantidade_cartas, 'npc')

# por todas as sprites aqui

placar_jogador = game.player_score
placar_computador = game.npc_score

# adiciona as 4 cartas a mao do jogador
for i in range(4):
    card = player_deck.comprar_carta()
    game.add_to_player_hand(card)

# adiciona os fundos dos placares
placar_jogador.add(elementos_tela.FundoPlacar(True))
placar_computador.add(elementos_tela.FundoPlacar(False))

rodando = True
clicked_card = None
click_enabled = True

while rodando:
    game.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not clicked_card and click_enabled:
            pos = pygame.mouse.get_pos()
            clicked_card_sprite = game.card_in(pos)
            if clicked_card_sprite:
                clicked_card = player_deck.get_by_id(clicked_card_sprite.id)

    if clicked_card:
        npc_card = npc_deck.comprar_carta()

        game.draw_played_cards(clicked_card, npc_card)

        # define ganhador da rodada
        ganhador = juiz.qual_carta_ganha_a_rodada_retorna_none_caso_empate(clicked_card, npc_card)

        # desenha placar
        if not ganhador is None:
            if ganhador:
                elemento_ganhador = npc_card.element
                if elemento_ganhador == 'fogo':
                    placar_computador.add(elementos_tela.Fogo(False))
                elif elemento_ganhador == 'agua':
                    placar_computador.add(elementos_tela.Agua(False))
                elif elemento_ganhador == 'gelo':
                    placar_computador.add(elementos_tela.Gelo(False))
            else:
                elemento_ganhador = clicked_card.element
                if elemento_ganhador == 'fogo':
                    placar_jogador.add(elementos_tela.Fogo(True))
                elif elemento_ganhador == 'agua':
                    placar_jogador.add(elementos_tela.Agua(True))
                else:
                    placar_jogador.add(elementos_tela.Gelo(True))

            juiz.contabiliza_no_placar_do_ganhador_da_rodada(ganhador, elemento_ganhador)

        print(f'Jogador: {clicked_card.element}')
        print(f'Computador: {npc_card}')
        print(f'Ganhador: {ganhador}')

        new_card = player_deck.comprar_carta()
        game.replace_player_hand(clicked_card_sprite, new_card)

        clicked_card = None

        if juiz.verifica_se_o_jogo_terminou():
            click_enabled = False

            game.draw_result_msg(juiz.quem_ganhou_a_jogo())

    game.draw()

pygame.quit()
