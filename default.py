import sys
import xbmcaddon
import xbmcgui
import xbmc
import random
from datetime import datetime
Addon = xbmcaddon.Addon('screensaver.clock')

__scriptname__ = Addon.getAddonInfo('name')
__path__ = Addon.getAddonInfo('path')


class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback
			
        def onScreensaverDeactivated(self):
            print '3 ExitMonitor: sending exit_callback'
            self.exit_callback()

    def onInit(self):
        print '2 Screensaver: onInit'
        self.monitor = self.ExitMonitor(self.exit)
	#hiding date if needed
	if Addon.getSetting('hidedate') == 'true':
		self.getControl(30106).setVisible(False)
	#do we want a background?
	if Addon.getSetting('enablebg') == 'true':
		self.getControl(30020).setImage(Addon.getSetting('backgroundlocation'))
	
	self.bouncespeed = int(Addon.getSetting('bouncespeed'))
	self.hour_control = self.getControl(30003)
	self.colon_control = self.getControl(30004)
	self.minute_control = self.getControl(30005)
	self.date_control = self.getControl(30106)
	self.container = self.getControl(30002)
	#bounce settings
	# The velocity, or distance moved per time step
	vx = random.randint(3,10)    # x velocity def=10
	vy = random.randint(3,10)    # y velocity def=5
	
	#color shit
	print 'Time color: %s' % Addon.getSetting('timecolor')
	if Addon.getSetting('timecolor') == "1": #gray
		self.hour_control.setColorDiffuse('0xC0848484')
		self.colon_control.setColorDiffuse('0xC0848484')
		self.minute_control.setColorDiffuse('0xC0848484')
	
	if Addon.getSetting('timecolor') == "2": #red
		self.hour_control.setColorDiffuse('0xC0FF0000')
		self.colon_control.setColorDiffuse('0xC0FF0000')
		self.minute_control.setColorDiffuse('0xC0FF0000')
	
	if Addon.getSetting('timecolor') == "3": #green
		self.hour_control.setColorDiffuse('0xC064FE2E')
		self.colon_control.setColorDiffuse('0xC064FE2E')
		self.minute_control.setColorDiffuse('0xC064FE2E')
	
	if Addon.getSetting('timecolor') == "4": #blue
		self.hour_control.setColorDiffuse('0xC02EFEF7')
		self.colon_control.setColorDiffuse('0xC02EFEF7')
		self.minute_control.setColorDiffuse('0xC02EFEF7')
	
	if Addon.getSetting('timecolor') == "5": #Purple
		self.hour_control.setColorDiffuse('0xC0FE2EF7')
		self.colon_control.setColorDiffuse('0xC0FE2EF7')
		self.minute_control.setColorDiffuse('0xC0FE2EF7')	
	
	while(True):
		#update time
		now  = datetime.now()
		hour = now.hour
		minute = now.minute
		screenx = self.getWidth()/2-200
		screeny = self.getHeight()/2-75
		self.minute_control.setImage('clock/%s.png'%minute)
		self.hour_control.setImage('clock/%s.png'%hour)
		#Random movements  movement = 1
		if Addon.getSetting('movement') == '1':
			new_x = random.randint(-screenx,screenx)
			new_y = random.randint(-screeny,screeny)
			self.container.setPosition(new_x,new_y)
			xbmc.sleep(3000)
		#Bounce movement=2
		if Addon.getSetting('movement') == '2':
			self.currentposition = self.container.getPosition()
			new_x = self.currentposition[0]+vx
			new_y = self.currentposition[1]+vy
			if new_x >= screenx or new_x <= -screenx:
				vx = vx*-1
			if new_y >= screeny or new_y <= -screeny:
				vy = vy*-1
			self.container.setPosition(new_x,new_y)
			xbmc.sleep(self.bouncespeed)
	
    def exit(self):
        print '4 Screensaver: Exit requested'
        self.close()


if __name__ == '__main__':
    print '1 Python Screensaver Started'
    screensaver_gui = Screensaver(
            'script-%s-main.xml' % __scriptname__,
            __path__,
            'default',
        )
    screensaver_gui.doModal()
    print '5 Python Screensaver Exited'
    del screensaver_gui
    sys.modules.clear()
