from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

window.vsync = False
app = Ursina()
wood = load_texture("assets/oak_planks.png")
stone = load_texture("assets/stone.png")
glass = load_texture("assets/glass.png")
grass = load_texture("assets/grass_block_top.png")
ctable = load_texture("assets/crafting_table.png")
door = load_texture("assets/door.png")
bed = load_texture("assets/red.png")
e = True
wood.filtering = None
stone.filtering = None
glass.filtering = None
grass.filtering = None
ctable.filtering = None
door.filtering = None
bed.filtering = None
breakblock = Audio('assets/stone1.ogg',autoplay=False,Loop=False)
music = Audio('assets/music/creative1.ogg',autoplay=True,Loop=False)

window.exit_button.visible = False
window.fullscreen = True

item = 1

def update():
    global item
    global music
    if held_keys['1']: item = 1
    if held_keys['2']: item = 2
    if held_keys['3']: item = 3
    if held_keys['4']: item = 4
    if held_keys['5']: item = 5
    if held_keys['6']: item = 6
    if held_keys['7']: item = 7
    if held_keys['8']: item = 8
    if not music.playing:
        music = Audio('assets/music/creative'+str(random.randint(1,6))+'.ogg',autoplay=True,Loop=False)

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = wood, color=color.white, model='cube', door = False, painting = False,MeshCollide=False):
        super().__init__(
            parent = scene,
            position = position,
            model = model,
            origin_y = 0.5,
            texture = texture,
            color = color
        )
        self.door = door
        if MeshCollide:
            self.collider = MeshCollider(self)
            self.model = load_model(model)
            self.y -= 1
        self.open = False
        self.painting = painting
        self.slab = False
    
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
                    voxel = Voxel(position = self.position+mouse.normal, texture=door, model='assets/door.obj',door=True,MeshCollide=True)
                if item == 7:
                    voxel = Voxel(position = self.position+mouse.normal, model='assets/painting.obj',painting=True,MeshCollide=True)
                if item == 8:
                    voxel = Voxel(position=self.position+mouse.normal, model='assets/bed.obj', texture=bed, MeshCollide=True)
            if key == 'left mouse down':
                breakblock.play()
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
            if key == 'p':
                if not self.slab:
                    self.scale = (1,0.5,1)
                    self.y -= 0.5
                else:
                    self.scale = (1,1,1)
                    self.y += 0.5
                self.slab = not self.slab

class Player(FirstPersonController):
    def __init__(self):
        super().__init__(jump_height=1)
        self.camera_pivot.y -= 0.25

for z in range(20):
    for x in range(20):
        voxel = Voxel(position = (x,0,z), texture=grass, color=color.green)

player = Player()

app.run()