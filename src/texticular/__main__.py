from game_controller import  Controller

controller = Controller()

controller.go()

while controller.state != "Game Over":
    controller.main_loop()



