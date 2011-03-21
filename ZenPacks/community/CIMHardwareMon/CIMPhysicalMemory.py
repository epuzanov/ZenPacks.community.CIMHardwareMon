################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMPhysicalMemory

CIMPhysicalMemory is an abstraction of a Memory module.

$Id: CIMPhysicalMemory.py,v 1.0 2011/03/21 22:16:12 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.MemoryModule import MemoryModule
from CIMComponent import *

class CIMPhysicalMemory(MemoryModule, CIMComponent):
    """PhysicalMemory object"""

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(CIMPhysicalMemory)
