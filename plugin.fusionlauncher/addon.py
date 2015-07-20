#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
import json
import urllib
import urllib2
import subprocess
import platform
import os.path

# magic; id of this plugin - cast to integer
thisPlugin = int(sys.argv[1])

addon = xbmcaddon.Addon();
addonname = addon.getAddonInfo("name");
addonID = addon.getAddonInfo('id')

fusionDir = addon.getSetting("cwd")
fusionCLI = fusionDir + "FusionCLI"

currentOS = platform.system()

if(not os.path.isfile(fusionCLI)):
    xbmcgui.Dialog().notification('Error!', 'Could not find FusionCLI-Executable. Please edit Settings!', xbmcgui.NOTIFICATION_ERROR) 
    exit()

def launchGame(gameID):
        if(currentOS == "Windows"):
                subprocess.Popen([fusionCLI, '--launch', gameID], cwd=fusionDir, shell=True)
        else:
                subprocess.Popen([fusionCLI + ' --launch ' + gameID], cwd=fusionDir, shell=True)

def parameters_string_to_dict(parameters):
        paramDict = {}
        if parameters:
                paramPairs = parameters[1:].split("&")
                for paramsPair in paramPairs:
                        paramSplits = paramsPair.split('=')
                        if (len(paramSplits)) == 2:
                                paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict

def showAllGames():
        global thisPlugin
        dataFile = ""

        if(currentOS == "Windows"):
                cli = subprocess.Popen([fusionCLI, '--allGames'],cwd=fusionDir, shell=True, stdout=subprocess.PIPE)
        else:
                cli = subprocess.Popen([fusionCLI + ' --allGames'],cwd=fusionDir, shell=True, stdout=subprocess.PIPE)

        while True:
                line = cli.stdout.readline()
                if len(line)>=1:
                        dataFile += line.rstrip()
                else:
                        break


        if len(dataFile)<=0:
            xbmcgui.Dialog().notification('Error!', 'Could not get Data from FusionCLI', xbmcgui.NOTIFICATION_ERROR) 
            exit()

        data = json.loads(dataFile);

        for Game in data['Games']:
                listItem = xbmcgui.ListItem(Game['name'])
                listItem.setArt({"banner": Game['banner'], "clearart": Game['clearart'], "clearlogo": Game['clearlogo'], "poster": Game['poster'], "thumbnail": Game['poster']})

                p= 'plugin://'+addonID+'/?action=launch&id='+Game['id']
                u = 'RunPlugin('+p+')'

                listItem.addContextMenuItems([("Launch", u,)])

                listItem.setThumbnailImage(Game['poster'])
                xbmcplugin.addDirectoryItem(thisPlugin,p,listItem)
        xbmcplugin.endOfDirectory(thisPlugin)



params = parameters_string_to_dict(sys.argv[2])
action = urllib.unquote_plus(params.get('action', ''))
id = urllib.unquote_plus(params.get('id', ''))

if action=='launch':
        launchGame(id)
else:
        showAllGames()