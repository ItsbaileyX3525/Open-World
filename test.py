from ursina import *

app=Ursina()

EditorCamera()
Entity(model='plane',texture='grass',scale=100)


def set_volume():
    global volume_slider
    volume = volume_slider.value
    print(volume)
    app.sfxManagerList[0].setVolume(volume)

volume_slider = Slider(min=0, max=100, default=100, dynamic=True,position=(-.25, .4),text='Master volume:',on_value_changed = set_volume)
info=Text(text='Restart to apply changes',size=.05,font="assets/misc/HighwayItalic-yad3.otf",y=-.3,x=-.25)

volume_slider.on_value_changed = set_volume

Audio('assets/audio/settings.ogg',autoplay=True)
Audio('assets/audio/intro.ogg',autoplay=True)
app.run()