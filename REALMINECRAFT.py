from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
#load all the texture
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/assets_punch_sound.wav', loop=False, autoplay=False)
block_pick = 1

#Για να μην φαινονται τα fps στη πανω γωνια
window.fps_counter.enable = False
#για να φυφει το exit button
window.exit_button.visible = False

def update():
    #για αλλαγη blocks που μπορω να βαλω
    global block_pick

    #Στο update methoud για να γινει η κινηση
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
    #dictionaries
    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4

class Voxel(Button):
    #Η κλαση Voxel ειναι για το πατωμα
    def __init__(self,position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            #Η ursina δεν εχει UV MAP αρα θα πρεπει να φτιαξουμε εμεισ ενα αντικειμανο που να εχει ωστε να κανουμε πανω του apply το texture
            model='assets/Grass_block_real',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
            )
    #για προσθηκη blocks
    def input(self, key):
        #το input του player
        if self.hovered:

            if key=='left mouse down':
                # Εδω για να παιξει ο ηχος
                punch_sound.play()
                #if για να επιλεξουμε ποιο απο τα block θα βαλουμε στο πατωμα
                if block_pick == 1:
                    voxel= Voxel(position=self.position+mouse.normal, texture=grass_texture)
                if block_pick == 2:
                    voxel= Voxel(position=self.position+mouse.normal, texture=stone_texture)
                if block_pick == 3:
                    voxel= Voxel(position=self.position+mouse.normal, texture=brick_texture)
                if block_pick == 4:
                    voxel= Voxel(position=self.position+mouse.normal, texture=dirt_texture)
            #καταστροφη blocks
            if key=='right mouse down':
                #Εδω για να παιξει ο ηχοσ οταν σπαμε τα blocks
                punch_sound.play()
                destroy(self)

#Κλασση ουρανου
class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            #Θελουμε double sided διοτι αν ειμαστε μεσα στο αντικειμενο δεν μπορουμε να το δουμε
            double_sided=True
            )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            #τα custom models εχουν προβλημα
            model='assets/arm_real',
            texture=arm_texture,
            scale=0.2,
            #Τοποθετηση χεριου στην οθονη
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6)
            )
    #τεχνιτο animation του χεριου οταν χτιζει
    #Στο active γινεται η κινηση
    def active(self):
        self.position=Vec2(0.3, -0.5)
    #Στο passive γινεται η επαναφορα
    def passive(self):
        self.position=Vec2(0.4, -0.6)



#ενθετη for για να χτιστουν τα τουβλακια σε δυο διαστασεις στο πατωμα
for z in range(25):
    for x in range(25):
        voxel = Voxel(position=(x, 0, z))

#FPS controlls
player = FirstPersonController()
#Δημιουργια ουρανου
sky = Sky()
#Δημιουργια χεριου
hand = Hand()

app.run()