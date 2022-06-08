from Classes.Game import Game
game = Game()
game.restart()
run = True
while run:
    run = game.tick()