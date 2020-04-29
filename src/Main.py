# @autor: Matheus Kunnen Ledesma - matheusl.2000@alunos.utfpr.edu.br

from sys import argv

from Scene01 import Scene01
from Scene02 import Scene02

class Main:
    

    # Scenes
    SCENE_01 = 1
    SCENE_02 = 2

    def __init__(self, scene_id = 1):
        self.scene = None
        if scene_id == Main.SCENE_01:
            self.scene = Scene01()
        elif scene_id == Main.SCENE_02:
            self.scene = Scene02()

        if self.scene is None:
            print("Invalid Scene!")
            exit(1)

    def run(self):
        self.scene.run()

if __name__ == "__main__":
    scene = None
    main = None

    # Check arguments
    if len(argv) > 1 and int(argv[1]) > 0:
        scene = int(argv[1])
        main = Main(scene)
    else :
        main = Main()

    main.run()

exit()