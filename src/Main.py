# @autor: Matheus Kunnen Ledesma - matheusl.2000@alunos.utfpr.edu.br

from sys import argv

from Scene01 import Scene01
from Scene02 import Scene02
from Scene03 import Scene03
from Scene04 import Scene04
from Scene05 import Scene05

class Main:
    
    # Scenes
    SCENE_01 = 1
    SCENE_02 = 2
    SCENE_03 = 3
    SCENE_04 = 4
    SCENE_05 = 5

    def __init__(self, scene_id = 1):
        self.scene = None
        if scene_id == Main.SCENE_01:
            self.scene = Scene01()
        elif scene_id == Main.SCENE_02:
            self.scene = Scene02()
        elif scene_id == Main.SCENE_03:
            self.scene = Scene03()
        elif scene_id == Main.SCENE_04:
            self.scene = Scene04()
        elif scene_id == Main.SCENE_05:
            self.scene = Scene05()

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