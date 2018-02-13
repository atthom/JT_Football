from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from .forms import *
from .sparq2html import Sparql2html


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)


class MapView(TemplateView):
    def get(self, request, **kwargs):
        ctx = dict()
        return render(request, 'map.html', context=ctx)


def queryView(request):
    form = QueryForm(request.POST or None)
    if form.is_valid():
        query = form.cleaned_data['textarea']
        sparql = Sparql2html(query)
        html = sparql.execute()
        return render(request, 'queryResult.html', context={"query": query, "result": html})
    return render(request, 'query.html', context={'form': form})
