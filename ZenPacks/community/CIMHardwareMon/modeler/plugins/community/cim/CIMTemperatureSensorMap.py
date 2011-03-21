################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMTemperatureSensorMap

CIMTemperatureSensorMap maps CIM_TemperatureSensor class to TemperatureSensor
class.

$Id: CIMTemperatureSensorMap.py,v 1.0 2011/03/21 22:03:36 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMTemperatureSensorMap(SQLPlugin):
    """Map CIM_TemperatureSensor class to TemperatureSensor class"""

    maptype = "CIMTemperatureSensorMap"
    modname = "ZenPacks.community.CIMHardwareMon.CIMTemperatureSensor"
    relname = "temperaturesensors"
    compname = "hw"
    deviceProperties = SQLPlugin.deviceProperties + ('zWinUser',
                                                    'zWinPassword',
                                                    'zCIMHWConnectionString',
                                                    )

    numericSensorTypes = {
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
                18:"Front Panel",
                19:"Back Panel",
                20:"IO Bus",
                21:"Peripheral Bay",
                22:"Device Bay",
                23:"Switch",
                24:"Software-defined",
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
            "CIM_TemperatureSensor":
                (
                "SELECT BaseUnits,ElementName,NumericSensorType,SensorType,UnitModifier,UpperThresholdCritical,UpperThresholdFatal,UpperThresholdNonCritical,__path FROM CIM_NumericSensor",
                None,
                cs,
                {
                    'BaseUnits':'baseUnits',
                    'ElementName':'id',
                    'NumericSensorType':'type',
                    'SensorType':'_sensorType',
                    'UnitModifier':'unitModifier',
                    'UpperThresholdCritical':'upperThresholdCritical',
                    'UpperThresholdFatal':'upperThresholdFatal',
                    'UpperThresholdNonCritical':'upperThresholdNonCritical',
                    '__path':'snmpindex',
                },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_TemperatureSensor", []):
            if instance['_sensorType'] != 2: continue
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            om.type = getattr(om, 'type', 0) or 0
            om.type = self.NumericSensorTypes.get(int(om.type), 'Unknown')
            if om.snmpindex.lower().startswith('root/ibmsd'): om.baseUnits = 2
            rm.append(om)
        return rm
