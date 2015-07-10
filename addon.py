import xbmcaddon
import xbmcgui
import xbmcplugin
import sys

thisPlugin = int(sys.argv[1])


addon = xbmcaddon.Addon();
addonname = addon.getAddonInfo("name");

def createListing():
	"""
	Creates a listing that XBMC can display as a directory listing
	@return list
	"""
	listing = []
	listing.append('The first item')
	listing.append('The second item')
	listing.append('The third item')
	listing.append('The fourth item')
	return listing


def sendToXbmc(listing):
	"""
	Sends a listing to XBMC for display as a directory listing
	Plugins always result in a listing
	@param list listing
	@return void
	"""
	#access global plugin id
	global thisPlugin
	# send each item to xbmc
	for item in listing:
		listItem = xbmcgui.ListItem(item)
		xbmcplugin.addDirectoryItem(thisPlugin,'',listItem)

	# tell xbmc we have finished creating the directory listing
	xbmcplugin.endOfDirectory(thisPlugin)

     
# Step 3 - run the program
sendToXbmc(createListing())

