from __future__ import unicode_literals

from django.db import models
from django.contrib.sites.models import Site
from django.core.urlresolvers import get_script_prefix
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import iri_to_uri, python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class BaseModel(models.Model):

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Environment(BaseModel):
    name = models.CharField(_('name'), max_length=20, db_index=True)
    domain = models.CharField(_('domain'), max_length=50, db_index=True)

class Role(BaseModel):
    name = models.CharField(_('name'), max_length=20, db_index=True)

class Variable(BaseModel):
    name = models.CharField(_('name'), max_length=50, db_index=True)
    value = models.CharField(_('value'), max_length=255, blank=True, null=True)

class Host(BaseModel):
    name = models.CharField(_('name'), max_length=255, db_index=True)
    env = models.ForeignKey(Environment, verbose_name=_('env'),
                    related_name="%(class)s_hosts", db_index=False, unique=False)
    roles = models.ManyToManyField(Role)
    variables = models.ManyToManyField(Variable)
