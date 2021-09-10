from menu import*
from intro import*
from game import*
new_game = "new_game"
resume = "resume"
m = Menu()
g=Game()
m.add_option("Resume", 500, 50, 512,300, resume)
m.add_option("New Game", 500, 50, 512,350,new_game)
m.run()
def start_game():
    while g.running:
        g.new()
        g.run()
        g.show_go_screen()

if m.command == new_game:
    g.show_start_screen()
    start_game()
elif m.command == resume:
    g.resume()
    start_game()

