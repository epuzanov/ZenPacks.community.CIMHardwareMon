################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMDiskDriveMap

CIMDiskDriveMap maps CIM_DiskDrive class to HardDisk class.

$Id: CIMDiskDriveMap.py,v 1.1 2011/03/22 22:26:21 egor Exp $"""

__version__ = '$Revision: 1.1 $'[11:-2]


from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CIMDiskDriveMap(SQLPlugin):
    """Map CIM_DiskDrive class to HardDisk"""

    maptype = "CIMDiskDriveMap"
    modname = "ZenPacks.community.CIMHardwareMon.CIMDiskDrive"
    relname = "harddisks"
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
            cs = cs + ",password='%s'"%getattr(device, 'zWinPassword', '')
        return {
            "CIM_DiskDrive":
                (
                "SELECT * FROM CIM_DiskDrive",
                None,
                cs,
                {
                    'DeviceID':'id',
                    'Manufacturer':'_manuf',
                    'MediaType':'_mediatype',
                    'Model':'setProductKey',
                },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_DiskDrive", []):
            if not str(instance.get('_mediatype', '')).startswith('Fixed'):
                continue
            om = self.objectMap(instance)
            om.id = self.prepId(om.id)
            try:
                om.snmpindex = perfnames.get(om.id, None)
                if not om.snmpindex: continue
                om.setProductKey = MultiArgs(om.setProductKey or 'Unknown',
                                        getattr(om, '_manuf', '') or 'Unknown')
            except AttributeError:
                continue
            rm.append(om)
        return rm
