from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

wood = load_texture("oak_planks.png")
stone = load_texture("stone.png")
glass = load_texture("glass.png")

window.exit_button.visible = False
window.fullscreen = True

item = 1

def update():
    global item
    if held_keys['1']: item = 1
    if held_keys['2']: item = 2
    if held_keys['3']: item = 3

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = wood):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = texture,
            color = color.white,
            highlight_color = color.white
        )
    
    def input(self,key):
        if self.hovered:
            if key == 'right mouse down':
                if item == 1:
                    voxel = Voxel(position = self.position+mouse.normal)
                if item == 2:
                    voxel = Voxel(position = self.position+mouse.normal, texture=stone)
                if item == 3:
                    voxel = Voxel(position = self.position+mouse.normal, texture=glass)
            if key == 'left mouse down':
                destroy(self)

class Player(FirstPersonController):
    def __init__(self):
        super().__init__(jump_height=1)
        self.camera_pivot.y -= 0.25

for z in range(20):
    for x in range(20):
        voxel = Voxel(position = (x,0,z))

player = Player()

app.run()