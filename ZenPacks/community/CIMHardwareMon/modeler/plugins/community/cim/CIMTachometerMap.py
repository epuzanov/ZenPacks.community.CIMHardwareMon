################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTachometerMap

CIMTachometerMap maps CIM_Tachometer class to CIMTachometer class.

$Id: CIMTachometerMap.py,v 1.1 2011/03/22 22:30:16 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMTachometerMap(SQLPlugin):
    """Map CIM_Tachometer class to Fan class"""

    maptype = "CIMTachometerMap"
    modname = "ZenPacks.community.CIMHardwareMon.CIMTachometer"
    relname = "fans"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMHWConnectionString',
                                                    )


    fanTypes = {0: 'Unknown',
                1: 'System Fan',
                2: 'Power Supply Fan',
                3: 'CPU Fan',
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
            "CIM_Tachometer":
                (
                "SELECT * FROM CIM_NumericSensor",
                None,
                cs,
                {
                    'Description':'description',
                    'ElementName':'id',
                    'FanType':'type',
                    'SensorType':'_sensorType',
                    'UnitModifier':'unitModifier',
                    'LowerThresholdCritical':'lowerThresholdCritical',
                    'LowerThresholdFatal':'lowerThresholdFatal',
                    'LowerThresholdNonCritical':'lowerThresholdNonCritical',
                    '__path':'snmpindex',
                },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_Tachometer", []):
            if instance['_sensorType'] != 5: continue
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.type = getattr(om, 'type', 0) or 0
            om.type = self.fanTypes.get(int(om.type), 'Unknown')
            rm.append(om)
        if len(rm.maps) > 0: return rm
        return
