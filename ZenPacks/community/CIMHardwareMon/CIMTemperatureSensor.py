################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTemperatureSensor

CIMTemperatureSensor is an abstraction of a temperature sensor or probe.

$Id: CIMTemperatureSensor.py,v 1.0 2011/03/21 22:20:41 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.TemperatureSensor import TemperatureSensor
from CIMComponent import *

class CIMTemperatureSensor(TemperatureSensor, CIMComponent):
    """TemperatureSensor object"""

    baseUnits = 2
    type = 'Unknown'
    unitModifier = 0
    upperThresholdCritical = 0
    upperThresholdFatal = 0
    upperThresholdNonCritical = 0

    _properties = TemperatureSensor._properties + (
                 {'id':'baseUnits', 'type':'int', 'mode':'w'},
                 {'id':'type', 'type':'string', 'mode':'w'},
                 {'id':'unitModifier', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdCritical', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdFatal', 'type':'int', 'mode':'w'},
                 {'id':'upperThresholdNonCritical', 'type':'int', 'mode':'w'},
                )

    def temperatureCelsius(self, default=None):
        """
        Return the current temperature in degrees celsius
        """
        temp = self.cacheRRDValue('CurrentReading', default)
        if temp is None: return None
        temp = 10 ** int(self.unitModifier or 0) * temp
        if self.baseUnits == 2: return long(temp)
        if self.baseUnits == 3: return long((temp - 32) / 9 * 5)
        if self.baseUnits == 4: return long(temp - 273.15)
        return long(temp)
    temperature = temperatureCelsius


    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates


InitializeClass(CIMTemperatureSensor)
