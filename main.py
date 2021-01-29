from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

window.vsync = False
app = Ursina()
wood = load_texture("assets/oak_planks.png")
stone = load_texture("assets/stone.png")
glass = load_texture("assets/glass.png")
grass = load_texture("assets/grass_block_top.png")
ctable = load_texture("assets/crafting_table.png")
door = load_texture("assets/door.png")
customtexture = load_texture('assets/oak_planks.png')
e = True
wood.filtering = None
stone.filtering = None
glass.filtering = None
grass.filtering = None
ctable.filtering = None
door.filtering = None

window.exit_button.visible = False
window.fullscreen = True

item = 1

def update():
    global item
    if held_keys['1']: item = 1
    if held_keys['2']: item = 2
    if held_keys['3']: item = 3
    if held_keys['4']: item = 4
    if held_keys['5']: item = 5
    if held_keys['6']: item = 6
    if held_keys['7']: item = 7

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = wood, color=color.white, model='cube', door = False, painting = False):
        super().__init__(
            parent = scene,
            position = position,
            model = model,
            origin_y = 0.5,
            texture = texture,
            color = color
        )
        self.door = door
        if door:
            self.y -= 1
            self.collider = MeshCollider(self)
        if painting:
            self.collider = MeshCollider(self)
        self.open = False
        self.painting = painting
    
    def input(self,key):
        if self.hovered:
            if key == 'right mouse down':
                if item == 1:
                    voxel = Voxel(position = self.position+mouse.normal)
                if item == 2:
                    voxel = Voxel(position = self.position+mouse.normal, texture=stone)
                if item == 3:
                    voxel = Voxel(position = self.position+mouse.normal, texture=glass)
                if item == 4:
                    voxel = Voxel(position = self.position+mouse.normal, texture=grass, color=color.green)
                if item == 5:
                    voxel = Voxel(position = self.position+mouse.normal, texture=ctable, model='assets/block.obj')
                if item == 6:
                    voxel = Voxel(position = self.position+mouse.normal, texture=door, model='assets/door.obj',door=True)
                if item == 7:
                    voxel = Voxel(position = self.position+mouse.normal, model='assets/painting.obj',painting=True)
            if key == 'left mouse down':
                destroy(self)
            if key == 'q':
                self.rotation_y += 90
            if key == 'e':
                if self.door:
                    if self.open:
                        self.model = load_model('assets/door.obj')
                        self.open = False
                    else:
                        self.model = load_model('assets/open_door.obj')
                        self.open = True
                    self.collider = MeshCollider(self)
                if self.painting:
                    self.texture = load_texture("paintings/"+input("image?"))
                    self.texture.filtering = None

class Player(FirstPersonController):
    def __init__(self):
        super().__init__(jump_height=1)
        self.camera_pivot.y -= 0.25

for z in range(20):
    for x in range(20):
        voxel = Voxel(position = (x,0,z), texture=grass, color=color.green)

player = Player()

app.run()