from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from .forms import CursusForm, QueryForm
from .sparq2html import Sparql2html
import json

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context={})


class MapView(TemplateView):
    def get(self, request, **kwargs):
        data = json.load(open("../static/data.json"))
        return render(request, 'map.html', context={"data": json.dumps(data)})


def dominanteView(request):
    if request.is_ajax() or request.method == 'POST':
       return render(request, 'dominante.html', context={"req": request})

    query = "select ?x ?y where {?x <http://polytech.unice.fr/cours/SI#estDansCursus> ?y}"
    sparql = Sparql2html(query)
    cours_dominante = sparql.raw_execute()
    cours = [row[0] for row in cours_dominante]
    return render(request, 'dominante.html', context={"cours": cours})
    

def queryView(request):
    form = QueryForm(request.POST or None)
    if form.is_valid():
        query = form.cleaned_data['textarea']
        sparql = Sparql2html(query)
        html = sparql.execute()
        return render(request, 'queryResult.html', context={"query": query, "result": html})
    return render(request, 'query.html', context={'form': form})


def cursusView(request):
    form = CursusForm(request.POST or None)
    if form.is_valid():
        dominante = form.cleaned_data['dominante']
        query = "select ?x where {?x <http://polytech.unice.fr/cours/SI#estDansCursus> ?y filter(?y=\":"
        query += dominante + "\")}"
        sparql = Sparql2html(query)
        cours = sparql.raw_execute()
        return render(request, 'cursusResult.html', context={"dominante": dominante, "cours": cours})
    return render(request, 'cursus.html', context={'form': form})
