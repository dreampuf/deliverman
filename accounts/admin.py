from datetime import datetime
from cStringIO import StringIO

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import forms
from django.contrib.auth import admin as auth_admin
from django.core.files.uploadedfile import InMemoryUploadedFile

import simpleldap
from PIL import Image

from accounts.models import User

class LDAPBackend(object):
    """
    Authenticate via LDAP.

    Use the login name, and a hash of the password. For example:

    LDAP_HOST = "LDAP_HOST"
    LDAP_DN = "LDAP_DN"
    LDAP_PASSWORD = "LDAP_PASSWORD"
    LDAP_BN = "LDAP_BN"
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
        is_new = False
        try:
            user = User.objects.get(username=entity["uid"][0])
        except User.DoesNotExist:
            is_new = True
            user = User(username=entity["uid"][0])
            user.is_staff = True
            user.is_superuser = False
            user.save()

        if password and user.check_password(password) is False:
            user.set_password(password)
        user.is_staff = True
        for k, kmap in (
                ("first_name", "givenName"),
                ("last_name", "sn"),
                ("email", "mail"),
                ("gid", "gidnumber"),
                ("uid", "uidnumber"),
                ("date_joined", "whencreated"),
                ("country", "co"),
                ("department", "department"),
                ("photo", "thumbnailphoto"),
                ):
            if k == "date_joined":
                val = datetime.strptime(entity.get(kmap)[0][:-3], "%Y%m%d%H%M%S")
            elif k == "photo" and is_new == True:
                photo_data = entity.get(kmap)[0]
                photo_io_origin = StringIO(photo_data)
                photo_img = Image.open(photo_io_origin)
                photo_side = min(photo_img.size)
                photo_croped = photo_img.crop((0, 0, photo_side, photo_side))
                photo_croped.thumbnail(settings.THUMBNAIL_SIZE_HEAD, Image.ANTIALIAS)
                photo_io_processed = StringIO()
                photo_croped.save(photo_io_processed, 'png')
                photo_io_origin.close()
                photo_io_processed.seek(0)

                val = InMemoryUploadedFile(
                        photo_io_processed,
                        None,
                        "{0}_{1}.png".format(user.first_name.lower(), user.last_name.lower()),
                        "image/png",
                        len(photo_data),
                        None
                    )
            else:
                val = entity.get(kmap)[0]
            if not val:
                continue
            setattr(user, k, val)
        user.save()
        return user

class UserCreationForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = ("username",)

class UserChangeForm(forms.UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

admin.site.register(User, UserAdmin)

