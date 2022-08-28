## CvGameInterfaceFile
##
## Overrides the use of CvGameUtils with BUG's modular game utils dispatcher.
##
## Copyright (c) 2009 The BUG Mod.
##
## Author: EmperorFool

import BugGameUtils
from Consts import *
GameUtils = BugGameUtils.getDispatcher()
