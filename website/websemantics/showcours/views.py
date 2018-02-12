from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class MapView(TemplateView):
    def get(self, request, **kwargs):
        ctx = dict()
        #ctx["foo"] = "bar"
        #ctx["request"] = request
        #ctx["kwargs"] = kwargs
        return render(request, 'map.html', context=ctx)


class QueryView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'query.html', context=None)
