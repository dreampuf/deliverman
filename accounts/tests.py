from django.test import TestCase

# Create your tests here.
class AccountsTestCase(TestCase):
    def test_ldapbackend(self):
        self.assertEqual(1, 1)
