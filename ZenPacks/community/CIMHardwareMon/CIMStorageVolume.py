################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMStorageVolume

CIMStorageVolume is an abstraction of a StorageVolume.

$Id: CIMStorageVolume.py,v 1.0 2011/03/21 22:12:35 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from ZenPacks.community.deviceAdvDetail.LogicalDisk import LogicalDisk
from CIMComponent import *

class CIMStorageVolume(LogicalDisk, CIMComponent):
    """StorageVolume object"""

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """

        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates

InitializeClass(CIMStorageVolume)
