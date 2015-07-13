import xbmcaddon
import xbmcgui
import xbmcplugin
import sys
import json

# magic; id of this plugin - cast to integer
thisPlugin = int(sys.argv[1])

addon = xbmcaddon.Addon();
addonname = addon.getAddonInfo("name");
#check
def createListing():
        listing = []
        listing.append('The first item')
        listing.append('The second item')
        listing.append('The third item')
        listing.append('The fourth item')
        return listing


def sendToXbmc():
        global thisPlugin

        with open('data.json') as dataFile:
                data = json.load(dataFile);

        for Game in data['Games']:
                listItem = xbmcgui.ListItem(Game['name'])
                listItem.setArt({"banner": Game['banner'], "clearart": Game['clearart'], "clearlogo": Game['clearlogo'], "poster": Game['poster'], "thumbnail": Game['poster']})
                listItem.setLabel(Game['name'])
                listItem.setThumbnailImage(Game['poster'])
                xbmcplugin.addDirectoryItem(thisPlugin,'',listItem)
        xbmcplugin.endOfDirectory(thisPlugin)


# Step 3 - run the program
sendToXbmc()

