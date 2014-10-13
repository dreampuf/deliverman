#from django.test import TestCase
import os
from unittest import TestCase

CURRENT_DIR = os.path.dirname(__file__)

text = """
[Prod:System]
ABC-dev[03:06,07,08!04,05,07:08].fwmrm.net

[Staging:Box]
ASHProxy01.fwmrm.net
ASHads[001:050]
ASHdbRep[01:02]
ASHDNSext[01:02]

PP[1:05]GG[10:15]CC

[Prod:Backup]
Backup01[02:03]

[Prod:Empty]

[dev:c2]

ASHdbRep[01:02]
Pek201.dev.fwmrm.net
"""

little_text = """
[ENV01:GROUP01]
WEB[01:03].domain
DB[01:10!3:9].domain
"""



# Create your tests here.
class InventoryTest(TestCase):
    def test_parser(self):
        from parser import deserialize, _ranger, _parse_tuple_item, _host_tuple_item
        self.assertEqual(
            list(_ranger("005", "10", "{:03d}")),
            ["005", "006", "007", "008", "009", "010"]
        )
        self.assertEqual(
            list(_parse_tuple_item("03:06,07:10,15")),
            ['3', '4', '5', '6', '7', '8', '9', '10', '15']
        )
        self.assertEqual(
            list(_host_tuple_item("03:06,07,08!04,05,07:08")),
            ['03', '06']
        )
        self.assertEqual(
            list(deserialize(little_text)),
            [
                ('SECTION', (u'ENV01', u'GROUP01')),
                ('HOST',
                 [u'WEB01.domain', u'WEB02.domain', u'WEB03.domain']
                 ),
                ('HOST',
                 [u'DB01.domain', u'DB02.domain', u'DB10.domain']
                 )
            ]
        )

