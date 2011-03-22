################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMPowerSupplyMap

CIMPowerSupplyMap maps CIM_PowerSupply CIM class to CIMPowerSupply class.

$Id: CIMPowerSupplyMap.py,v 1.1 2011/03/21 22:29:05 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMPowerSupplyMap(SQLPlugin):
    """Map CIM_PowerSupply class to PowerSupply class"""

    maptype = "CIMPowerSupplyMap"
    modname = "ZenPacks.community.CIMHardwareMon.CIMPowerSupply"
    relname = "powersupplies"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMHWConnectionString',
                                                    )


    powerSupplyTypes = {
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
            18:"Compute Cabinet Bulk Power Supply",
            19:"Compute Cabinet System Backplane Power Supply",
            20:"Compute Cabinet I/O chassis enclosure Power Supply",
            21:"Compute Cabinet AC Input Line",
            22:"I/O Expansion Cabinet Bulk Power Supply",
            23:"I/O Expansion Cabinet System Backplane Power Supply",
            24:"I/O Expansion Cabinet I/O chassis enclosure Power Supply",
            25:"I/O Expansion Cabinet AC Input Line",
            26:"Peripheral Bay",
            27:"Device Bay",
            28:"Switch",
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
            cs = cs + ",password='%s'"%getattr(device, 'zWinPassword', '')
        return {
            "CIM_PowerSupply":
                (
                "SELECT * FROM CIM_PowerSupply",
                None,
                cs,
                {
                    'DeviceID':'id',
                    'PowerSupplyType':'type',
                    'TotalOutputPower':'watts',
                    '__path':'snmpindex',
                },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_PowerSupply", []):
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.type = getattr(om, 'type', 0) or 0
            om.type = self.powerSupplyTypes.get(int(om.type), 'Unknown')
            if om.watts: om.watts = int(om.watts) / 1000
            rm.append(om)
        return rm


