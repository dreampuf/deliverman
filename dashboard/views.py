from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required

#from models import inventory_parser

class BaseView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)

class IndexView(BaseView):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        return super(IndexView, self).get(request, *args, **kwargs)

class DeployView(BaseView):
    template_name = "index.html"

class InventoryView(BaseView):
    template_name = "inventory.html"
    def get(self, request, *args, **kwargs):
        return super(InventoryView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print request
        return super(InventoryView, self).post(request, *args, **kwargs)


class ProjectView(BaseView):
    template_name = "index.html"
