from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class MapView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'map.html', context=None)


class QueryView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'query.html', context=None)
