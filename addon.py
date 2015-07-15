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

# magic; id of this plugin - cast to integer
thisPlugin = int(sys.argv[1])

addon = xbmcaddon.Addon();
addonname = addon.getAddonInfo("name");
addonID = addon.getAddonInfo('id')

fusionDir = addon.getSetting("cwd")
fusionCLI = fusionDir + "FusionCLI"



def launchGame(gameID):
        param = '--launch ' + gameID
        xbmcgui.Dialog().ok(addonname, param, fusionCLI, fusionDir);
        subprocess.Popen([fusionCLI, param],cwd=fusionDir, shell=True);

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
        param = '--allGames'
        cli =  subprocess.Popen([fusionCLI, param],cwd=fusionDir, shell=True, stdout=subprocess.PIPE)
        while True:
          line = cli.stdout.readline()
          if len(line)>=1:
                dataFile += line.rstrip()
          else:
                break

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
