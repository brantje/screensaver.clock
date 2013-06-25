import sys
import xbmcaddon
import xbmcgui
import xbmc
import random
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
	if Addon.getSetting('movement') == '1':
		#Random movements
		while(True):
			container = self.getControl(30002)
			screenx = self.getWidth()/2-175
			screeny = self.getHeight()/2-75
			print 'Screen X : %s' % screenx	
			print 'Screen Y : %s' % screeny	
			new_x = random.randint(-screenx,screenx)
			new_y = random.randint(-screeny,screeny)

			container.setPosition(new_x,new_y)
			xbmc.sleep(3000)
	
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
