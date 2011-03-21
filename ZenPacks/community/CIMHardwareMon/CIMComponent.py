################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMStatus

CIMStatus is an abstraction for OperationalStatus Property.

$Id: CIMStatus.py,v 1.0 2010/03/12 14:45:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.deviceAdvDetail.HWStatus import *
from Products.ZenModel.ZenossSecurity import *

class CIMComponent(HWStatus):

    statusmap ={0: (DOT_GREY, SEV_WARNING, 'Unknown'),
                1: (DOT_GREY, SEV_WARNING, 'Other'),
                2: (DOT_GREEN, SEV_CLEAN, 'OK'),
                3: (DOT_ORANGE, SEV_ERROR, 'Degraded'),
                4: (DOT_YELLOW, SEV_WARNING, 'Stressed'),
                5: (DOT_YELLOW, SEV_WARNING, 'Predictive Failure'),
                6: (DOT_ORANGE, SEV_ERROR, 'Error'),
                7: (DOT_RED, SEV_CRITICAL, 'Non-Recoverable Error'),
                8: (DOT_BLUE, SEV_INFO, 'Starting'),
                9: (DOT_YELLOW, SEV_WARNING, 'Stopping'),
                10: (DOT_ORANGE, SEV_ERROR, 'Stopped'),
                11: (DOT_BLUE, SEV_INFO, 'In Service'),
                12: (DOT_GREY, SEV_WARNING, 'No Contact'),
                13: (DOT_ORANGE, SEV_ERROR, 'Lost Communication'),
                14: (DOT_ORANGE, SEV_ERROR, 'Aborted'),
                15: (DOT_GREY, SEV_WARNING, 'Dormant'),
                16: (DOT_ORANGE, SEV_ERROR, 'Stopping Entity in Error'),
                17: (DOT_GREEN, SEV_CLEAN, 'Completed'),
                18: (DOT_YELLOW, SEV_WARNING, 'Power Mode'),
                }

    def getRRDTemplates(self):
        """
        Return the RRD Templates list
        """
        templates = []
        for tname in [self.__class__.__name__]:
            templ = self.getRRDTemplateByName(tname)
            if templ: templates.append(templ)
        return templates
