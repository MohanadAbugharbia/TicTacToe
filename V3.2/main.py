import pygame
from game import Game
from AI import AI

game = Game()
ai = AI()
run = True

clock = pygame.time.Clock()
winner = game.check_for_winner(game.game_board)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not winner:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pos[1] >= 200:
                        if game.get_mouse(pos[0] // 133, (pos[1] - 200) // 133):
                            if game.tiles_taken == 9:
                                game.no_winner_draw()
                                run = False
                            else:
                                game.make_move(pos[0] // 133, (pos[1] - 200) // 133, game.turn)
                                winner = game.check_for_winner(game.game_board)
                            if not winner:
                                if game.tiles_taken == 9:
                                    game.no_winner_draw()
                                    run = False
                                else:
                                    ai_move = ai.generate_Move(game)
                                    game.make_move(ai_move[0], ai_move[1], game.turn)
                                    winner = game.check_for_winner(game.game_board)
                            else:
                                run = False
                                break
    clock.tick(20)
    game.draw()
    pygame.display.flip()

if winner:
    print(f"Player {winner} has won the game!")
