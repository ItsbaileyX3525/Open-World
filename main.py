from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from ursina.prefabs.first_person_controller import FirstPersonController
from panda3d.core import Loader
from ursina import *
from direct.interval.IntervalGlobal import LerpHprInterval
from direct.interval.ActorInterval import LerpAnimInterval
from ursina.prefabs.health_bar import HealthBar
import json


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

class BillBoy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=scene,model=None, position=(5,0,0),rotation=(0,0,0),scale=2,collider='box',**kwargs)
        self.actor=Actor(BillNPC)
        self.actor.reparentTo(self)
        self.actor.loop("idle")
        self.actor.setPos(0,0,1.6)
        self.current_anim=None
        self.collider=BoxCollider(entity=self, size=(.5,3.9,.5))

    def LerpAnim(self,toanim,rate=1,part=None,loop=True):
        current=self.actor.get_current_anim()
        self.actor.enableBlend()
        self.actor.setPlayRate(rate,toanim,partName=part)
        if toanim==self.current_anim:
            pass     
        elif self.current_anim!=None:
            if loop:
                self.actor.loop(toanim, partName=part)
                Interv=LerpAnimInterval(self.actor, 0.25, self.current_anim, toanim, partName=part)
                Interv.start()
            else:
                self.actor.play(toanim, partName=part)
                Interv=LerpAnimInterval(self.actor, 0.25, self.current_anim, toanim, partName=part)
                Interv.start()
        elif self.current_anim==None:
            if loop:
                self.actor.loop(toanim, partName=part)
                Interv=LerpAnimInterval(self.actor, 0.25, current, toanim, partName=part)
                Interv.start()
            else:
                self.actor.play(toanim, partName=part)
                Interv=LerpAnimInterval(self.actor, 0.25, current, toanim, partName=part)
                Interv.start()     
        else: #This part doesnt work
            print(f"No animtion with name {toanim} found")
        self.current_anim=toanim


    def input(self,key):
        dist=distance_2d(Harlod.position, self.position)
        if dist<=3:
            if key=='e':
                self.LerpAnim("talk",loop=False)
                mouse.locked=False
                application.paused=True
                Text(text='Hello, How are you?',y=-.1,x=-.1)
                BillConversation1.play()
                invoke(self.default,delay=4)
                NextDialouge=Button(text="I'm ok.",scale_y=.1,scale_x=.2)


    def default(self):
        self.LerpAnim('idle')
    def update(self):
        pass
LoadingText=Text(text='Loading assets',enabled=False,x=-.7,y=.45)

loadedmodels=0

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

def GameStart():
    global Harlod,loadedmodels
    if loadedmodels>=2:
        destroy(MainMenu)
        DefaultPlayArea=Entity(model='plane',scale=1000,texture='grass',collider='box',texture_scale=(31.6227766017,31.6227766017))
        Harlod=FirstPersonController()
        IntroMusic.stop()
        destroy(GameLogo)
        ply=Character()
        BillLad=BillBoy()
        destroy(MainMenuSettings)
        destroy(MainMenuStart)
        destroy(MainMenuQuit)
    else:
        GameAssets=Text(text='Game assets are still loading',x=-.15,y=.1)
        destroy(GameAssets,delay=1)

def ChangeVsync():
    global vsyncEnabled
    if vsyncEnabled:
        vsyncEnabled=False
        VsyncSetting.text=f'Vsync: off'
        print(vsyncEnabled)
        data["vsyncEnabled"] = False
        info=Text(text='Restart to apply changes',size=.05,font="assets/misc/HighwayItalic-yad3.otf",y=-.3,x=-.25)
        destroy(info,delay=3)
        with open("data.json", "w") as f:
            json.dump(data, f)
    else:
        vsyncEnabled=True
        VsyncSetting.text=f'Vsync: on'
        data["vsyncEnabled"] = True
        info=Text(text='Restart to apply changes',size=.05,font="assets/misc/HighwayItalic-yad3.otf",y=-.3,x=-.25)
        destroy(info,delay=3)
        with open("data.json", "w") as f:
            json.dump(data, f)

volume=1
def set_volume():
    global volume_slider,volume
    volume = volume_slider.value/100
    print(volume)
    app.sfxManagerList[0].setVolume(volume)
    volume = volume
    print(volume)
def ChangeScreen():
    global Fullscreen
    if Fullscreen:
        window.fullscreen=False
        Fullscreen=False
        FullscreenSetting.text=f'Fullscreen: off'
        data['Fullscreen'] = False
        with open("data.json", "w") as f:
            json.dump(data, f)
    else:
        window.fullscreen=True
        Fullscreen=True
        FullscreenSetting.text=f'Fullscreen: on'
        data['Fullscreen'] = True
        with open("data.json", "w") as f:
            json.dump(data, f)
def SettingsMenu():
    global VsyncSetting,volume_slider,volume,FullscreenSetting
    MainMenuStart.disabled=True; MainMenuStart.visible=False
    GameLogo.visible=False
    IntroMusic.stop(); SettingsMusic.play()
    MainMenuSettings.on_click=SettingsMenuReturn; MainMenuSettings.text='Return'; MainMenuSettings.y=-.3
    if vsyncEnabled:
        VsyncSetting=Button(text=f'Vsync: on',scale_x=.2,scale_y=.1,y=.3,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeVsync)
    else:
        VsyncSetting=Button(text=f'Vsync: off',scale_x=.2,scale_y=.1,y=.3,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeVsync)
    MainMenuQuit.visible=False; MainMenuQuit.disabled=True
    volume_slider = Slider(min=0, max=100, default=volume*100, dynamic=True,position=(-.25, .4),text='Master volume:',on_value_changed = set_volume)
    if Fullscreen:
        FullscreenSetting=Button(text=f'Fullscreen: on',scale_x=.2,scale_y=.1,y=.2,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeScreen)
    else:
        FullscreenSetting=Button(text=f'Fullscreen: off',scale_x=.2,scale_y=.1,y=.2,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeScreen)

def SettingsMenuReturn():
    MainMenuSettings.on_click=SettingsMenu; MainMenuSettings.text='Settings'; MainMenuSettings.y=-.1
    MainMenuStart.disabled=False; MainMenuStart.visible=True
    SettingsMusic.stop(); IntroMusic.play()
    GameLogo.visible=True
    destroy(VsyncSetting); destroy(volume_slider); destroy(FullscreenSetting)
    MainMenuQuit.visible=True; MainMenuQuit.disabled=False
    

def logo2():
    global GameLogo
    camera.overlay.color = color.black
    logoB = Sprite(name='assets/misc/bluey', parent=camera.ui, texture='bluey', world_z=camera.overlay.z-1, scale=.1, color=color.clear)
    logoB.animate_color(color.white, duration=2, delay=1, curve=curve.out_quint_boomerang)
    camera.overlay.animate_color(color.clear, duration=1, delay=4)
    destroy(logoB, delay=4)
    GameLogo=Sprite(texture='assets/misc/servents.png',scale=1,y=2.2)
    invoke(QUETHEMUSIC,delay=5)

def QUETHEMUSIC():
    IntroMusic.play()

"""with open('functions.py', 'r') as func:
    file_contents=func.read()
    exec(file_contents)"""

with open("data.json", 'r') as f:
    data=json.load(f)

global vsyncEnabled,Fullscreen,CurrentLevel,cheese
vsyncEnabled=data['vsyncEnabled']
Fullscreen=data['Fullscreen']
CurrentLevel=data['CurrentLevel']
cheese=data['cheese']

print(vsyncEnabled)




window.vsync=vsyncEnabled
window.fullscreen=Fullscreen

if cheese:
    while True:
        print("CHEESE!")
app=Ursina(borderless=False)

camera.overlay.color = color.black
logo = Sprite(name='ursina_splash', parent=camera.ui, texture='ursina_logo', world_z=camera.overlay.z-1, scale=.1, color=color.clear)
logo.animate_color(color.white, duration=2, delay=1, curve=curve.out_quint_boomerang)
destroy(logo, delay=5)
invoke(logo2,delay=3)


MainMenu=Entity(model='quad',color=color.black66,scale=100)
MainMenuStart=Button(text='Start Game',scale_y=.1,scale_x=.2,color=color.clear,highlight_color=color.clear,x=-.7,on_click=GameStart)
MainMenuSettings=Button(text='Settings',scale_y=.1,scale_x=.2,color=color.clear,hightlight_color=color.clear,x=-.7,y=-.12,on_click=SettingsMenu)
MainMenuQuit=Button(text='Quit to desktop',scale_y=.1,scale_x=.2,color=color.clear,hightlight_color=color.clear,x=-.7,y=-.4,on_click=application.quit)

TempEntity=Entity(y=-999999999999999999999)

#Model loading
app.taskMgr.add(LoadModel(model="assets/game/player.glb",name="Player",parent=TempEntity))
app.taskMgr.add(LoadModel(model="assets/game/bill.glb",name="BillNPC",parent=TempEntity))

#Audio loading
app.taskMgr.add(LoadAudio(path="assets/audio/intro.ogg",name="IntroMusic",loop=True))
app.taskMgr.add(LoadAudio(path="assets/audio/settings.ogg",name="SettingsMusic",loop=True))
app.taskMgr.add(LoadAudio(path="assets/NPC/Bill/BillConversation1.ogg",name="BillConversation1",loop=False))
app.run(info=False)