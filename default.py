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
        self.bouncespeed = int(float(Addon.getSetting('bouncespeed')))
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
                
       #kleur = ['0xCFFFFFFF','0xC0848484','0xC0FF0000','0xC064FE2E','0xC02EFEF7','0xC0FE2EF7']
        kleur = ['0xC0FFFFFF','0xC0F0F8FF','0xC0FAEBD7','0xC000FFFF','0xC07FFFD4','0xC0F0FFFF','0xC0F5F5DC','0xC0FFE4C4','0xC0000000','0xC0FFEBCD','0xC00000FF','0xC08A2BE2','0xC0A52A2A','0xC0DEB887','0xC05F9EA0','0xC07FFF00','0xC0D2691E','0xC0FF7F50','0xC06495ED','0xC0FFF8DC','0xC0DC143C','0xC000FFFF','0xC000008B','0xC0008B8B','0xC0B8860B','0xC0A9A9A9','0xC0006400','0xC0BDB76B','0xC08B008B','0xC0556B2F','0xC0FF8C00','0xC09932CC','0xC08B0000','0xC0E9967A','0xC08FBC8F','0xC0483D8B','0xC02F4F4F','0xC000CED1','0xC09400D3','0xC0FF1493','0xC000BFFF','0xC0696969','0xC01E90FF','0xC0B22222','0xC0FFFAF0','0xC0228B22','0xC0FF00FF','0xC0DCDCDC','0xC0F8F8FF','0xC0FFD700','0xC0DAA520','0xC0808080','0xC0008000','0xC0ADFF2F','0xC0F0FFF0','0xC0FF69B4','0xC0CD5C5C','0xC04B0082','0xC0FFFFF0','0xC0F0E68C','0xC0E6E6FA','0xC0FFF0F5','0xC07CFC00','0xC0FFFACD','0xC0ADD8E6','0xC0F08080','0xC0E0FFFF','0xC0FAFAD2','0xC0D3D3D3','0xC090EE90','0xC0FFB6C1','0xC0FFA07A','0xC020B2AA','0xC087CEFA','0xC0778899','0xC0B0C4DE','0xC0FFFFE0','0xC000FF00','0xC032CD32','0xC0FAF0E6','0xC0FF00FF','0xC0800000','0xC066CDAA','0xC00000CD','0xC0BA55D3','0xC09370D8','0xC03CB371','0xC07B68EE','0xC000FA9A','0xC048D1CC','0xC0C71585','0xC0191970','0xC0F5FFFA','0xC0FFE4E1','0xC0FFE4B5','0xC0FFDEAD','0xC0000080','0xC0000000','0xC0FDF5E6','0xC0808000','0xC06B8E23','0xC0FFA500','0xC0FF4500','0xC0DA70D6','0xC0EEE8AA','0xC098FB98','0xC0AFEEEE','0xC0D87093','0xC0FFEFD5','0xC0FFDAB9','0xC0CD853F','0xC0FFC0CB','0xC0DDA0DD','0xC0B0E0E6','0xC0800080','0xC0FF0000','0xC0BC8F8F','0xC04169E1','0xC08B4513','0xC0FA8072','0xC0F4A460','0xC02E8B57','0xC0FFF5EE','0xC0A0522D','0xC0C0C0C0','0xC087CEEB','0xC06A5ACD','0xC0708090','0xC0FFFAFA','0xC000FF7F','0xC04682B4','0xC0D2B48C','0xC0008080','0xC0D8BFD8','0xC0FF6347','0xC040E0D0','0xC0EE82EE','0xC0F5DEB3','0xC0F5F5F5','0xC0FFFF00','0xC09ACD32']
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