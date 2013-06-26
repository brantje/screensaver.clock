#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Sander Brand (brantje@brantje.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
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
            self.exit_callback()

    def onInit(self):
        self.log('INIT')
        self.abort_requested = False
        self.started = False
        self.exit_monitor = self.ExitMonitor(self.exit)

        self.bouncespeed = int(Addon.getSetting('bouncespeed'))
        self.hour_control = self.getControl(30003)
        self.colon_control = self.getControl(30004)
        self.minute_control = self.getControl(30005)
        self.date_control = self.getControl(30106)
        self.container = self.getControl(30002)
	    #hiding date if needed
        if Addon.getSetting('hidedate') == 'true':
		    self.getControl(30106).setVisible(False)
	    #do we want a background?
        if Addon.getSetting('enablebg') == 'true':
            self.getControl(30020).setImage(Addon.getSetting('backgroundlocation'))
	
        self.vx = random.randint(3,10)    # x velocity def=10
        self.vy = random.randint(3,10)    # y velocity def=5
        if Addon.getSetting('timecolor') == "1": #gray
            self.hour_control.setColorDiffuse('0xC0848484')
            self.colon_control.setColorDiffuse('0xC0848484')
            self.minute_control.setColorDiffuse('0xC0848484')
        if Addon.getSetting('timecolor') == "2": #red
            self.hour_control.setColorDiffuse('0xC0FF0000')
            self.colon_control.setColorDiffuse('0xC0FF0000')
            self.minute_control.setColorDiffuse('0xC0FF0000')
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
        self.DisplayTime()


    def DisplayTime(self):
        while not self.abort_requested:
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
                new_x = self.currentposition[0]+self.vx
                new_y = self.currentposition[1]+self.vy
                if new_x >= screenx or new_x <= -screenx:
                    self.vx = self.vx*-1
                if new_y >= screeny or new_y <= -screeny:
                    self.vy = self.vy*-1
                self.container.setPosition(new_x,new_y)
                xbmc.sleep(self.bouncespeed)      
		if self.abort_requested:
			self.log('slideshow abort_requested')
			self.exit()
			return
		xbmc.sleep(500)

    def exit(self):
        self.abort_requested = True
        self.exit_monitor = None
        self.log('exit')
        self.close()

    def log(self, msg):
        xbmc.log(u'Clock Screensaver: %s' % msg)


if __name__ == '__main__':
    screensaver = Screensaver(
        'script-%s-main.xml' % __scriptname__,
        __path__,
        'default',
    )
    screensaver.doModal()
    del screensaver
    sys.modules.clear()