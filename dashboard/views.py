from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import get_user

class IndexView(TemplateView):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        kwargs["user"] = user
        return super(IndexView, self).get(request, *args, **kwargs)

class DeployView(TemplateView):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        kwargs["user"] = user
        return super(IndexView, self).get(request, *args, **kwargs)

class InventoryView(TemplateView):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        kwargs["user"] = user
        return super(IndexView, self).get(request, *args, **kwargs)

class ProjectView(TemplateView):
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        kwargs["user"] = user
        return super(IndexView, self).get(request, *args, **kwargs)
