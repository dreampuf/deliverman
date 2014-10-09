from django.test import TestCase

# Create your tests here.
class ModelTest(TestCase):
    def test_relationship(self):
        from dashboard.models import Environment, Role, Variable, Host
        env, _ = Environment.objects.get_or_create(
            name="prod",
            domain="fwmrm.net",
        )

        role1, _ = Role.objects.get_or_create(name="RPM-RE")
        role2, _ = Role.objects.get_or_create(name="RPM-UI")

        var1, _ = Variable.objects.get_or_create(name="enable", value="False")
        var2, _ = Variable.objects.get_or_create(name="public", value="True")
        var3, _ = Variable.objects.get_or_create(name="logo_url", value="http://0.jpg")

        host1, _ = Host.objects.get_or_create(
            name="rpm-elt01",
            env=env
        )
        host1.roles.add(role1)
        host1.variables.add(var1, var2)
        host2, _ = Host.objects.get_or_create(
            name="rpm-web01",
            env=env
        )
        host2.roles.add(role1, role2)
        host2.variables.add(var1, var3)

