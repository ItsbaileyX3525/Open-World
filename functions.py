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
        DefaultPlayArea=Entity(model='plane',scale=1000,texture='grass',collider='box')
        Harlod=FirstPersonController()
        IntroMusic.stop()
        destroy(GameLogo)
        ply=Character()
        BillLad=BillBoy()
        destroy(MainMenuSettings)
        destroy(MainMenuStart)
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
        info=Text(text='Restart to apply changes', font="HighwayItalic-yad3.otf",y=-.3,x=-.1)
        destroy(info,delay=3)
        with open("data.json", "w") as f:
            json.dump(data, f)
    else:
        vsyncEnabled=True
        VsyncSetting.text=f'Vsync: on'
        data["vsyncEnabled"] = True
        info=Text(text='Restart to apply changes', font="HighwayItalic-yad3.otf",y=-.3,x=-.1)
        destroy(info,delay=3)
        with open("data.json", "w") as f:
            json.dump(data, f)
def SettingsMenu():
    global VsyncSetting
    MainMenuStart.disabled=True; MainMenuStart.visible=False
    GameLogo.visible=False
    IntroMusic.stop(); SettingsMusic.play()
    MainMenuSettings.on_click=SettingsMenuReturn; MainMenuSettings.text='Return'; MainMenuSettings.y=-.3
    if vsyncEnabled:
        VsyncSetting=Button(text=f'Vsync: on',scale_x=.2,scale_y=.1,y=.3,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeVsync)
    else:
        VsyncSetting=Button(text=f'Vsync: off',scale_x=.2,scale_y=.1,y=.3,x=-.35,color=color.clear,highlight_color=color.clear,on_click=ChangeVsync)
    MainMenuQuit.visible=False; MainMenuQuit.disabled=True

def SettingsMenuReturn():
    MainMenuSettings.on_click=SettingsMenu; MainMenuSettings.text='Settings'; MainMenuSettings.y=-.1
    MainMenuStart.disabled=False; MainMenuStart.visible=True
    SettingsMusic.stop(); IntroMusic.play()
    GameLogo.visible=True
    VsyncSetting.disabled=True; VsyncSetting.visible=False
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