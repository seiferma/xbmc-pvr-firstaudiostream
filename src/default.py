'''
Copyright 2014 Stephan Seifermann

This file is part of xbmc-pvr-firstaudiostream.

xbmc-pvr-firstaudiostream is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 2 of the License, or (at your option) any later
version.

xbmc-pvr-firstaudiostream is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along with
xbmc-pvr-firstaudiostream. If not, see http://www.gnu.org/licenses/.
'''

import json
import xbmc, xbmcaddon

__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

def logDebug(message):
    xbmc.log(__addonname__ + ": " + message, xbmc.LOGDEBUG)

def executeJsonRequest(methodName, parameters=dict()):
    request = {"jsonrpc": "2.0", "method": methodName, "params": parameters, "id": 42}
    return executeJson(request)

def executeJson(cmdDict):
    cmdString = json.dumps(cmdDict)
    resultString = xbmc.executeJSONRPC(cmdString)
    return json.loads(resultString)

def changeAudioStreamIfNecessary():
    if not xbmc.getCondVisibility("VideoPlayer.Content(livetv)"):
        return
    
    playersResult = executeJsonRequest("Player.GetActivePlayers")
    activeVideoPlayerId = -1
    for player in playersResult["result"]:
        if player["type"] == "video":
            activeVideoPlayerId = player["playerid"]
    if activeVideoPlayerId == -1:
        return
    
    audioStreamResult = executeJsonRequest("Player.GetProperties",
                                           {"playerid" : activeVideoPlayerId,
                                            "properties" : ["currentaudiostream"]})
    if audioStreamResult["result"]["currentaudiostream"]["index"] != 0:
        audioStreamChangeResult = executeJsonRequest("Player.SetAudioStream",
                                                     {"playerid" : activeVideoPlayerId,
                                                      "stream" : 0})
        logDebug("Changed audio stream (" + audioStreamChangeResult["result"] + ")")

def main():
    logDebug("Started service")
    while (not xbmc.abortRequested):
        xbmc.sleep(10000)
        changeAudioStreamIfNecessary()
    logDebug("Stopped service")

if __name__ == '__main__':
    main()
