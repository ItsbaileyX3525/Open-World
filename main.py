from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from ursina.prefabs.first_person_controller import FirstPersonController
from panda3d.core import Loader
from ursina import *
from direct.interval.ActorInterval import LerpAnimInterval
from ursina.prefabs.health_bar import HealthBar
import pickle

class Character(AnimatedEntity):
    def __init__(self, **kwargs):
        super().__init__(parent=Harlod,model=Player, position=(0,.9,1),rotation=(0,180,0),scale=0.018,**kwargs)
        self.loop("idle")
        self.speedRegenBoost=1
        self.walkSpeed=6
        self.runSpeed=17
        self.jogSpeed=12
        self.swiftness=1
        self.health_regen_timer=0
        self.sprint_bar = HealthBar(bar_color=color.yellow, roundness=.5,value=100,z=100,animation_duration=0)
        self.current_anim=None

    def input(self, key):
        if key=='w':
            self.LerpAnim(toanim="walk")
        elif key=='w' and held_keys['shift']:
            self.LerpAnim(toanim="run")
        elif held_keys['w'] and key=='shift':
            self.LerpAnim(toanim="run")
        elif held_keys['shift'] and key=='s':
            self.LerpAnim(toanim="walk backwards")
        elif held_keys['shift'] and key=='w':
            self.LerpAnim(toanim="walk")
        elif key=='a':
            self.LerpAnim(toanim="strafe left")
        elif key=='d':
            self.LerpAnim(toanim="strafe right")
        elif key=='s':
            self.LerpAnim(toanim="walk backwards")
        elif key=='s' and held_keys['shift']:
            self.LerpAnim(toanim="run backwards")
        elif key=='shift' and held_keys['s']:
            self.LerpAnim(toanim="run backwards")
        elif key == 'd up' and not held_keys['a'] and not held_keys['s'] and not held_keys['w']:
            self.LerpAnim(toanim="idle")
        elif key == 'a up'and not held_keys['d'] and not held_keys['s'] and not held_keys['w']:
            self.LerpAnim(toanim="idle")
        elif key == 's up'and not held_keys['a'] and not held_keys['d'] and not held_keys['w']:
            self.LerpAnim(toanim="idle")
        elif key == 'w up'and not held_keys['a'] and not held_keys['s'] and not held_keys['d']:
            self.LerpAnim(toanim="idle")
        elif key=='shift up' and held_keys['w']:
            self.LerpAnim(toanim="walk")
        elif key=='shift up' and held_keys['s']:
            self.LerpAnim(toanim="walk backwards")
        if key=='f':
            self.sprint_bar.max_value+=20
            self.speedRegenBoost+=1
            self.swiftness+=1
    def update(self):
        if held_keys['shift'] and held_keys['w'] and not held_keys['s']:
            if self.sprint_bar.value == 0:
                Harlod.speed = self.walkSpeed * self.swiftness
            else:
                Harlod.speed = self.runSpeed * self.swiftness
                self.sprint_bar.value -= 0.25
                self.health_regen_timer = 0
        elif held_keys['shift'] and held_keys['s'] and not held_keys['w']:
            if self.sprint_bar.value == 0:
                Harlod.speed = self.walkSpeed * self.swiftness
            else:
                Harlod.speed = self.jogSpeed
                self.sprint_bar.value -= 0.25
                self.health_regen_timer = 0
        elif self.health_regen_timer >= 2:
            if self.sprint_bar.value < self.sprint_bar.max_value:
                self.sprint_bar.value += .1 * self.speedRegenBoost
                Harlod.speed = self.walkSpeed * self.swiftness
        else:
            Harlod.speed = self.walkSpeed * self.swiftness
            self.health_regen_timer += time.dt
            

LoadingText=Text(text='Loading assets',enabled=False,x=-.7,y=.45)



async def LoadModel(model, name=None,parent=scene): #Smoothly loads models
    global LoadingText,modelname,loadedmodels
    LoadingText.enabled=True
    modelname=name
    modelname = await loader.loadModel(model, blocking=False)
    globals()[name] = modelname
    LoadingText.enabled=False
    loadedmodels+=1


async def LoadAudio(path, name=None,autoplay=False,loop=False): #Smoothly loads audio files
    global LoadingText,audioname
    LoadingText.enabled=True
    audioname = loader.loadSfx(path)
    
    audioname=Audio(audioname,autoplay=autoplay,loop=loop)
    globals()[name] = audioname
    LoadingText.enabled=False


loadedmodels=0

def GameStart():
    global Harlod
    if loadedmodels<=2:
        destroy(MainMenu)
        DefaultPlayArea=Entity(model='plane',scale=1000,texture='grass',collider='box')
        Harlod=FirstPersonController()
        IntroMusic.stop()
        destroy(GameLogo)
        ply=Character()
        destroy(MainMenuStart)

    else:
        GameAssets=Text(text='Game assets are still loading',x=-.15,y=.1)
        destroy(GameAssets,delay=1)

try:
    with open('Prefrences.dat','rb') as pref:
        isVsync=pickle.load(pref)
except Exception:
    isVsync=input("Vsync on or off? (Choice will be saved and can be changed later) ")
    with open('Prefrences.dat','wb') as pref:
        pickle.dump(isVsync, pref)

if isVsync=='on':
    window.vsync=True
elif isVsync=='off':
    window.vsync=False
else:
    print("failed to set vsync")
window.show_ursina_splash=False
app=Ursina(borderless=False)
def logo2():
    camera.overlay.color = color.black
    logoB = Sprite(name='bluey', parent=camera.ui, texture='bluey', world_z=camera.overlay.z-1, scale=.1, color=color.clear)
    logoB.animate_color(color.white, duration=2, delay=1, curve=curve.out_quint_boomerang)
    camera.overlay.animate_color(color.clear, duration=1, delay=4)
    destroy(logoB, delay=4)
    invoke(QUETHEMUSIC,delay=5)

def QUETHEMUSIC():
    global GameLogo
    IntroMusic.play()
    GameLogo=Sprite(texture='servents.png',scale=.8,y=2.2)

camera.overlay.color = color.black
logo = Sprite(name='ursina_splash', parent=camera.ui, texture='ursina_logo', world_z=camera.overlay.z-1, scale=.1, color=color.clear)
logo.animate_color(color.white, duration=2, delay=1, curve=curve.out_quint_boomerang)
destroy(logo, delay=5)
invoke(logo2,delay=3)







MainMenu=Entity(model='quad',color=color.black66,scale=100)
MainMenuStart=Button(text='Start Game',scale_y=.1,scale_x=.2,on_click=GameStart)

TempEntity=Entity(y=-999999999999999999999)

#Model loading
app.taskMgr.add(LoadModel(model="player.glb",name="Player",parent=TempEntity))
app.taskMgr.add(LoadModel(model="player1.gltf",name="LoadAmount",parent=TempEntity))

#Audio loading
app.taskMgr.add(LoadAudio(path="intro.ogg",name="IntroMusic",loop=True))

app.run(info=False)