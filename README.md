xbmc-pvr-firstaudiostream
=========================

# Purpose
This XBMC addon automatically switches to the first audio stream when watching live tv. This circumvents the audio stream selection mechanisms of the PVR backend/client or XBMC.

# Building
Simply execute the build.py module. It will create a folder containing all relevant files and a zip file, which can easily be installed in XBMC.

# Usage
Install the addon in XBMC. It requires no configuration or activation, but a restart of XBMC might be required. Please note that switching the audio stream may take up to 10 seconds because of API limitations.