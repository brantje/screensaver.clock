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
        self.background = self.getControl(30020)
        self.hour_control = self.getControl(30003)
        self.colon_control = self.getControl(30004)
        self.minute_control = self.getControl(30005)
        self.ampm_control = self.getControl(30007)
        self.date_control = self.getControl(30106)
        self.container = self.getControl(30002)
        self.configmultibackground = self.getControl(30107)
        self.waitcounter = 0
        #show colon
        self.colon_control.setImage('clock/colon.png')
        #hiding date if needed
        if Addon.getSetting('hidedate') == 'true':
             self.date_control.setVisible(False)
        #do we want a background?
        if Addon.getSetting('enablebg') == '1':
            self.background.setImage(Addon.getSetting('backgroundlocation'))
        if Addon.getSetting('enablebg') == '2':
            self.configmultibackground.setLabel(Addon.getSetting('backgroundlocationdir'))
    
        self.vx = random.randint(3,10) # x velocity def=10
        self.vy = random.randint(3,10) # y velocity def=5
        ccolor = self.SetClockColor(Addon.getSetting('timecolor'))
        self.DisplayTime()
        

    def DisplayTime(self):
        while not self.abort_requested:
            #update time
            now  = datetime.now()
            hour = now.hour
            minute = now.minute
            screeny = 720-self.container.getHeight()
            if Addon.getSetting('ampm') == "false":
                screenx = 1280-self.container.getWidth() #830 self.getWidth()/2-200
            else:
                screenx = 1280-self.container.getWidth()-100 #830 self.getWidth()/2-200
            
                
            if Addon.getSetting('twentyfour') == "false" and hour > 12:
                hour -= 12
                if Addon.getSetting('ampm') == "true":
                    self.ampm_control.setImage('clock/pm.png')
            else:
                if Addon.getSetting('ampm') == "true":
                    self.ampm_control.setImage('clock/am.png')
            #Set the time
            
            self.minute_control.setImage('clock/%s.png'%minute)
            self.hour_control.setImage('clock/%s.png'%hour)
            self.date_control.setLabel(now.strftime("%A, %d %B %Y"))
            
            #no movements
            if Addon.getSetting('movement') == '0':
                new_x = screenx/2
                new_y = screeny/2
                self.container.setPosition(new_x,new_y)
                self.ColonBlink()
                xbmc.sleep(500)			
            #Random movements  movement = 1
            if Addon.getSetting('movement') == '1':
                
                if self.waitcounter == 5:
                    new_x = random.randint(-40,screenx)
                    new_y = random.randint(-50,screeny)
                    self.container.setPosition(new_x,new_y)
                    self.waitcounter = 0
                else:
                    self.waitcounter += 1
                
                self.ColonBlink()
                xbmc.sleep(500)
            #Bounce movement=2
            if Addon.getSetting('movement') == '2':
                self.currentposition = self.container.getPosition()
                new_x = self.currentposition[0]+self.vx
                new_y = self.currentposition[1]+self.vy
                if new_x >= screenx or new_x <= -40:
                    self.vx = self.vx*-1
                if new_y >= screeny or new_y <= -50:
                    self.vy = self.vy*-1
                self.container.setPosition(new_x,new_y)
                self.ColonBlink()
                xbmc.sleep(self.bouncespeed) 
                    
        if self.abort_requested:
            self.log('Clock abort_requested')
            self.exit()
            return

    def ColonBlink(self):
        if Addon.getSetting('colonblink') == 'true':
            second = datetime.now().second
            if second%2==0:
                self.colon_control.setVisible(True)
            else:
                self.colon_control.setVisible(False)
        else:
            self.colon_control.setVisible(True)
    def SetClockColor(self,a):
        a = int(a)
        kleur = ['0xCFFFFFFF','0xC0848484','0xC0FF0000','0xC064FE2E','0xC02EFEF7','0xC0FE2EF7']
        self.log('Color selected: %s'%kleur[a])
        self.hour_control.setColorDiffuse(kleur[a])
        self.colon_control.setColorDiffuse(kleur[a])
        self.minute_control.setColorDiffuse(kleur[a])
        self.ampm_control.setColorDiffuse(kleur[a])
    
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