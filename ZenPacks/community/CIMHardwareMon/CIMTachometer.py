################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTachometer

CIMTachometer is an abstraction of a tachometer.

$Id: CIMTachometer.py,v 1.0 2011/03/21 22:19:05 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.Fan import Fan
from CIMComponent import *

class CIMTachometer(Fan, CIMComponent):
    """Tachometer object"""

    description = ''
    unitModifier = 0
    lowerThresholdCritical = 0
    lowerThresholdFatal = 0
    lowerThresholdNonCritical = 0

    _properties = Fan._properties + (
                 {'id':'description', 'type':'string', 'mode':'w'},
                 {'id':'unitModifier', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdCritical', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdFatal', 'type':'int', 'mode':'w'},
                 {'id':'lowerThresholdNonCritical', 'type':'int', 'mode':'w'},
                )


    def rpm(self, default=None):
        """
        Return the current RPM
        """
        rpm = self.cacheRRDValue('CurrentReading', default)
        if rpm is None: return None
        return 10 ** int(self.unitModifier or 0) * rpm


    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates


InitializeClass(CIMTachometer)
