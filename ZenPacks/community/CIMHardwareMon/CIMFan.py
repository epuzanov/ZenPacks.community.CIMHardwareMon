################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMFan

CIMFan is an abstraction of a Fan.

$Id: CIMFan.py,v 1.0 2011/03/21 22:13:57 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Products.ZenModel.Fan import Fan
from CIMComponent import *

class CIMFan(Fan, CIMComponent):
    """Fan object"""

    def rpmString(self, default=None):
        """
        Return a string representation of the RPM
        """
        return self.getStatus() == 0 and 'Normal' or 'unknown'


    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates


InitializeClass(CIMFan)
