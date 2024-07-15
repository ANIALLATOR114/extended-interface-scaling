# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/account_helpers/settings_core/InterfaceScaleManager.py
import weakref
import Event
import BigWorld
from gui.shared.utils import graphics
from gui import g_guiResetters
from account_helpers.settings_core import settings_constants
from helpers import dependency
from skeletons.connection_mgr import IConnectionManager


class InterfaceScaleManager(object):
    connectionMgr = dependency.descriptor(IConnectionManager)
    onScaleChanged = Event.Event()
    onScaleExactlyChanged = Event.Event()

    def __init__(self, settingsCore):
        self.proxy = weakref.proxy(settingsCore)
        self.__index = None
        self.__scaleValue = None
        return

    def init(self):
        g_guiResetters.add(self.scaleChanged)
        self.connectionMgr.onConnected += self.scaleChanged
        self.connectionMgr.onDisconnected += self.scaleChanged
        self.proxy.onSettingsChanged += self.onSettingsChanged
        self.scaleChanged()

    def fini(self):
        self.connectionMgr.onDisconnected -= self.scaleChanged
        self.connectionMgr.onConnected -= self.scaleChanged
        self.proxy.onSettingsChanged -= self.onSettingsChanged
        g_guiResetters.discard(self.scaleChanged)

    def get(self):
        return self.__scaleValue

    def getIndex(self):
        return self.__index

    def onSettingsChanged(self, diff):
        if settings_constants.GRAPHICS.INTERFACE_SCALE in diff:
            index = diff[settings_constants.GRAPHICS.INTERFACE_SCALE]
            self.changeScale(index)

    def scaleChanged(self):
        index = self.proxy.getSetting(settings_constants.GRAPHICS.INTERFACE_SCALE)
        self.changeScale(index)

    def changeScale(self, index):
        self.__index = index
        prevScaleValue = self.__scaleValue
        self.__scaleValue = self.getScaleByIndex(self.__index)
        self.onScaleChanged(self.__scaleValue)
        graphics.onInterfaceScaleChanged(self.__scaleValue)
        if prevScaleValue != self.__scaleValue:
            self.onScaleExactlyChanged(self.__scaleValue)

    @staticmethod
    def getScaleOptions():
        return graphics.getInterfaceScalesList(BigWorld.screenSize())

    def getScaleByIndex(self, ind):
        scaleOptions = self.getScaleOptions()

        if ind < 0 or ind >= len(scaleOptions):
            return 1.0
        
        scaleString = scaleOptions[int(ind)]
        return float(scaleString[1:])
