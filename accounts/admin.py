from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

#from accounts.models import User, UserManager

#admin.site.register(UserManager, User)
# unregister the Group model from admin.
#admin.site.unregister(Group)

import simpleldap
from django.conf import settings
from django.contrib.auth.models import User, check_password

class LDAPBackend(object):
    """
    Authenticate via LDAP.

    Use the login name, and a hash of the password. For example:

    LDAP_HOST = "pekdc01.freewheelmedia.net"
    LDAP_DN = "cn=readonly,dc=freewheelmedia,dc=net"
    LDAP_PASSWORD = "XXX"
    LDAP_BN = "ou=User Accounts,dc=freewheelmedia,dc=net"
    LDAP_UID = "cn={user}"
    """

    def authenticate(self, username=None, password=None):
        with simpleldap.Connection(settings.LDAP_HOST) as conn:
            login_valid = conn.authenticate(dn="%s,%s" % (settings.LDAP_UID.format(user=username), settings.LDAP_BN), password=password)
        if login_valid is False:
            self._set_active(username, False)
            return None

        with simpleldap.Connection(settings.LDAP_HOST, dn=settings.LDAP_DN, password=settings.LDAP_PASSWORD) as conn:
            try:
                rets = conn.search("(%s)" % (settings.LDAP_UID.format(user=username), ) , base_dn=settings.LDAP_BN)
            except simpleldap.ObjectNotFound:
                self._set_active(username, False)
                return None
            self._set_active(username, True)
            ldap_user = rets[0]
        user = self._user_from_ldap(ldap_user, password)
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _set_active(self, username, is_active=False):
        try:
            user = User.objects.get(username=username)
            user.is_active = is_active
            user.save()
        except User.DoesNotExist:
            pass

    def _user_from_ldap(self, entity, password=None):
        """
        from vision import Visicon
        img = Visicon(ip, str(time()), size).draw_image()
        temp_img = StringIO()
        img.save(temp_img, 'png')
        img_data = temp_img.getvalue()
        temp_img.close()
        """
        try:
            user = User.objects.get(username=entity["uid"][0])
            user.first_name = entity["givenName"][0]
            if password and user.check_password(password) is False:
                user.set_password(password)
            user.is_staff = True
            for k, kmap in (
                    ("first_name", "givenName"),
                    ("last_name", "sn"),
                    ("email", "mail"),
                    ):
                val = entity.get(kmap)
                if not val:
                    continue
                setattr(user, k, val[0])
            user.save()
            return user
        except User.DoesNotExist:
            user = User(username=entity["uid"][0])
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = False
            user.save()
        return user

