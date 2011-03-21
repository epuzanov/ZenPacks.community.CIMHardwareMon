################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMFanMap

CIMFanMap maps CIM_Fan class to HardDisk class.

$Id: CIMFanMap.py,v 1.0 2011/03/21 21:15:32 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.CIMDataSource.CIMPlugin import CIMPlugin

class CIMFanMap(CIMPlugin):
    """Map CIM_Fan class to Fan class"""

    maptype = "CIMFanMap"
    modname = "ZenPacks.community.CIMHardwareMon.CIMFan"
    relname = "fans"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMHWConnectionString',
                                                    )


    def queries(self, device):
        cs = getattr(device,
                    'zCIMHWConnectionString',
                    "'pywbemdb',scheme='https',port=5989,namespace='root/cimv2'")
        options = [opt.split('=')[0].strip().lower() for opt in cs.split(',')]
        if 'host' not in options:
            cs = cs + ",host='%s'"%device.manageIp
        if 'user' not in options:
            cs = cs + ",user='%s'"%getattr(device, 'zWinUser', '')
        if 'password' not in options:
            cs = cs + ",user='%s'"%getattr(device, 'zWinPassword', '')

    fanTypes = {
        0: "Unknown",
        1: "Other",
        2: "System board",
        3: "Host System board",
        4: "I/O board",
        5: "CPU board",
        6: "Memory board",
        7: "Storage bays",
        8: "Removable Media Bays",
        9: "Power Supply Bays",
        10:"Ambient / External / Room",
        11:"Chassis",
        12:"Bridge Card",
        13:"Management board",
        14:"Remote Management Card",
        15:"Generic Backplane",
        16:"Infrastructure Network",
        17:"Blade Slot in Chassis/Infrastructure",
        18:"Cabinet blower",
        19:"Compute Cabinet I/O Fans",
        20:"I/O Expansion Cabinet Utility Chassis Fan",
        21:"I/O Expansion Cabinet I/O Fan",
        22:"Processor Fan",
        23:"Cell Fan",
        24:"Cooling Device",
        25:"Front Panel",
        26:"Back Panel",
        27:"IO Bus",
        28:"Peripheral Bay",
        29:"Device Bay",
        30:"Switch",
        31:"Software-defined",
        }

    coolingDeviceTypes = {
        1: "Other",
        2: "Unknown",
        3: "Fan",
        4: "Centrifugal Blower",
        5: "Chip Fan",
        6: "Cabinet Fan",
        7: "Power Supply Fan",
        8: "Heap Pipe",
        9: "Integrated Refrigeration",
        32:"Active Cooling",
        33:"Passive Cooling",
        }

    def queries(self, device):
        cs = getattr(device,
                    'zCIMHWConnectionString',
                    "'pywbemdb',scheme='https',port=5989,namespace='root/cimv2'")
        options = [opt.split('=')[0].strip().lower() for opt in cs.split(',')]
        if 'host' not in options:
            cs = cs + ",host='%s'"%device.manageIp
        if 'user' not in options:
            cs = cs + ",user='%s'"%getattr(device, 'zWinUser', '')
        if 'password' not in options:
            cs = cs + ",user='%s'"%getattr(device, 'zWinPassword', '')
        return {
            "CIM_Fan":
                (
                "SELECT CoolingDeviceType,DeviceID,FanType,__path FROM CIM_Fan",
                None,
                cs,
                {
                    'CoolingDeviceType':'_type',
                    'DeviceID':'id',
                    'FanType':'type',
                    '__path':'snmpindex',
                },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_Fan", []):
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.type = getattr(om, 'type', 0) or 0
            if om.type == 0:
                om.type = getattr(om, '_type', 0) or 0
                om.type = self.coolingDeviceTypes.get(int(om.type), 'Unknown')
            else: om.type = self.fanTypes.get(int(om.type), 'Unknown')
            rm.append(om)
        if len(rm.maps) > 0: return rm
        return
