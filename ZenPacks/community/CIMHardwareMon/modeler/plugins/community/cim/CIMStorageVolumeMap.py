################################################################################
#
# This program is part of the CIMHardwareMon Zenpack for Zenoss.
# Copyright (C) 2011 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CIMStorageVolumeMap

CIMStorageVolumeMap maps CIM_StorageVolume class to LogicalDisk class.

$Id: CIMStorageVolumeMap.py,v 1.0 2011/03/21 21:51:14 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from ZenPacks.community.SQLDataSource.SQLPlugin import SQLPlugin

class CIMStorageVolumeMap(SQLPlugin):
    """Map CIM_StorageVolume class to LogicalDisk"""

    maptype = "CIMStorageVolumeMap"
    modname = "ZenPacks.community.CIMHardwareMon.CIMLogicalDisk"
    relname = "logicaldisks"
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
            "CIM_StorageVolume":
                (
                "SELECT * FROM CIM_StorageVolume",
                None,
                cs,
                {
                    '__path':'snmpindex',
                    'BlockSize':'_blocksize',
		    'DataRedundancy':'_dr',
                    'DeviceID':'id',
                    'ElementName':'description',
                    'NumberOfBlocks':'_blocks',
                    'StripeSize':'stripesize',
                },
                ),
            }

    def process(self, device, results, log):
        """collect CIM information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        rm = self.relMap()
        for instance in results.get("CIM_StorageVolume", []):
            try:
                om = self.objectMap(instance)
                om.id = self.prepId(om.id)
                if om._blocksize and om._blocks:
                    om.size = int(om._blocksize) * int(om._blocks)
            except AttributeError:
                continue
            rm.append(om)
        return rm
