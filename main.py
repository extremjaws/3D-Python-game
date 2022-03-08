import random
try:
    from ursina import *
    from ursina.prefabs.first_person_controller import FirstPersonController
except:
    print("Could not find ursina package.")
    print("Starting ursina install - will only work if you have python 3.8 32 bit installed in the default location.")
    os.startfile("ursinaInstaller.lnk")
    print("Started insalling ursina, when the pip window closes, resart this.")
    while True:
        time.sleep(1)

parkour = []
difficulty = int(input("parkour difficulty: "))
cheatInput = input("Cheat bridge (y/n)? ")
nbipin = input("No placing in parkour (y/n)? ")
if nbipin == 'y': nbip = True
else: nbip = False
if cheatInput == 'y': cheat = True
else: cheat = False
window.vsync = False
app = Ursina()
wood = load_texture("assets/oak_planks.png")
stone = load_texture("assets/stone.png")
glass = load_texture("assets/glass.png")
grass = load_texture("assets/grass_block_top.png")
ctable = load_texture("assets/crafting_table.png")
door = load_texture("assets/door.png")
bed = load_texture("assets/red.png")
jukebox = load_texture("assets/jukebox.png")
e = True
wood.filtering = None
stone.filtering = None
glass.filtering = None
grass.filtering = None
ctable.filtering = None
door.filtering = None
bed.filtering = None
jukebox.filtering = None
breakblock = Audio('assets/stone1.ogg',autoplay=False,Loop=False)

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
    if held_keys['9']: item = 9
    if held_keys['0']: item = 0
    if player.position.y <=-10:
        player.position = (8.5,1.5,20)
        player.velocity = 0
    if held_keys['=']:
        print("Removing blocks from old parkour...")
        for i in parkour:
            destroy(i)
        makePk()
    if held_keys['-']:
        difficulty = int(input("parkour difficulty: "))
        print("Removing blocks from old parkour...")
        for i in parkour:
            destroy(i)
        makePk()

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = wood, color=color.white, model='cube', door = False, painting = False,MeshCollide=False,music=False):
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
        self.music = music
    
    def input(self,key):
        if self.hovered:
            if key == 'right mouse down':
                zpos = mouse.position.z+self.position.z
                if not 20 <= zpos <= 319 and round(zpos,2)==zpos or not nbip:
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
                    if item == 9:
                        voxel = Voxel(position = self.position+mouse.normal, texture=jukebox, model='assets/block.obj', music=True)
                    if item == 0:
                        voxel = Voxel(position = self.position+mouse.normal, texture=grass, color=color.red)
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
                if self.music:
                    music = Audio('music/'+input("song?")+'.ogg',autoplay=True,Loop=False)
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
        super().__init__(jump_height=1.1)
        self.camera_pivot.y -= 0.25
def makePk():
    print("Starting generation of new parkour...")
    for z in range(300):
        for x in range(20):
            if random.randint(1,difficulty+1) == 1:
                parkour.append(Voxel(position = (x,0,z+21), texture=stone))
    print("Finished generation new parkour")
    #try: pkText
    #except NameError: pkText=None
    #if pkText is not None: destroy(pkText)
    #pkText = Text(text="parkour voxel count: {num}".format(num=str(len(parkour))),scale=1)
    #pkText.position = (-0.89,0.49)

for z in range(20):
    for x in range(20):
        voxel = Voxel(position = (x,0,z), texture=grass, color=color.green)
        if random.randint(0,1) == 1:
            voxel = Voxel(position = (x,5,z), texture=stone)
for y in range(6):
    for x in range(20):
        voxel = Voxel(position = (x,y,-1), texture=stone)
        #voxel = Voxel(position = (x+1,y,20), texture=stone)
        voxel = Voxel(position = (x,0,20),texture=grass, color=color.green)
    for z in range(20):
        voxel = Voxel(position = (-1,y,z), texture=stone)
        voxel = Voxel(position = (20,y,z), texture=stone)


for z in range(5):
    for x in range(20):
        voxel = Voxel(position = (x,0, z+320), texture=grass, color=color.gold)

#cheat bridge - can be commented out.   
if cheat:
    for z in range(305):
        Voxel(position=(20,0,z+20),texture=wood)
voxel = Voxel(position = (10,1,324), texture=jukebox, model='assets/block.obj', music=True)

makePk()
player = Player()
app.run()
loading.destroy()
