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

import os, shutil
import zipfile
import xml.dom.minidom

__BUILD_DIR__ = "build"
__SOURCE_DIR__ = "src"

class AddonDescription(object):
    def __init__(self, addonRoot):
        self.xml = xml.dom.minidom.parse(os.path.join(addonRoot, "addon.xml"))
        
    def getId(self):
        return self.xml.getElementsByTagName("addon")[0].getAttribute("id")
        
    def getVersion(self):
        return self.xml.getElementsByTagName("addon")[0].getAttribute("version")


def zipDir(path, zipFile):
    for root, _, files in os.walk(path):
        for f in files:
            zipFile.write(os.path.join(root, f),
                          os.path.relpath(os.path.join(root, f), os.path.join(path, "..")))

def getZipFileName(addonDescription):
    return addonDescription.getId() + "-" + addonDescription.getVersion() + ".zip"

def main():
    deploymentDir = os.path.abspath(__BUILD_DIR__)
    sourceDir = os.path.abspath(__SOURCE_DIR__)
    
    if os.path.exists(deploymentDir):
        shutil.rmtree(deploymentDir)

    addonDescription = AddonDescription(sourceDir)
    deploymentDirTmp = os.path.join(deploymentDir, addonDescription.getId())
    
    shutil.copytree(sourceDir, deploymentDirTmp)
    shutil.copy("LICENSE", os.path.join(deploymentDirTmp, "LICENSE.txt"))
    
    zipf = zipfile.ZipFile(os.path.join(deploymentDir, getZipFileName(addonDescription)), 'w')
    zipDir(deploymentDirTmp, zipf)
    zipf.close()

if __name__ == '__main__':
    main()