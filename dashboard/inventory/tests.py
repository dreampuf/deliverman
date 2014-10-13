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

from dashboard.models import Environment, Role, Host
from parser import store, deserialize, _ranger, _parse_tuple_item, _host_tuple_item

# Create your tests here.
class InventoryTest(TestCase):
    def test_parser(self):
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

    def test_model_store(self):
        self.assertEqual(store(deserialize(little_text)), None)

    def test_host_text_change_effect_store(self):
        text_1 = """
        [ENV1:GROUP1]
        WEB[1,2,3].domain
        DB[01:03].domain
        [ENV2:GROUP2]
        DB[5:08].domain
        """
        self.assertEqual(store(deserialize(text_1)), None)
        env1_group1_entities = Host.objects.filter(env__name="ENV1", roles__name="GROUP1")
        self.assertEqual(
            map(lambda x: x.name, env1_group1_entities),
            [
                u'WEB1.domain', u'WEB2.domain', u'WEB3.domain',
                u'DB01.domain', u'DB02.domain', u'DB03.domain'
            ]
        )
        # test add a server
        text_2 = """
        [ENV1:GROUP1]
        WEB[1,2,3,4].domain
        DB[01:03].domain
        [ENV2:GROUP2]
        DB[5:08].domain
        """
        self.assertEqual(store(deserialize(text_2)), None)
        env1_group1_entities_new = Host.objects.filter(env__name="ENV1", roles__name="GROUP1")
        #TODO

        # test move a server
        text_3 = """
        [ENV1:GROUP1]
        WEB[1,2,3].domain
        DB[01:03].domain
        [ENV2:GROUP2]
        WEB[4].domain
        DB[5:08].domain
        """
        self.assertEqual(store(deserialize(text_3)), None)
        env1_group1_entities_new = Host.objects.filter(env__name="ENV1", roles__name="GROUP1")
        #TODO

        # test remove a server
        #TODO

