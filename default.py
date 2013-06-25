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
	if Addon.getSetting('hidedate') == 'true':
		self.getControl(30106).setVisible(False)
	print 'Setting: %s' % Addon.getSetting('movement')
	
	self.hour_control = self.getControl(30003)
	self.minute_control = self.getControl(30005)	
	self.container = self.getControl(30002)
	#bounce settings
	# The velocity, or distance moved per time step
	vx = 10    # x velocity
	vy = 5    # y velocity
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
			xbmc.sleep(100)
	
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
