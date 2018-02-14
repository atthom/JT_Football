# howdy/urls.py
#from django.conf.urls import url
#from showcours import views

# urlpatterns = [
#    url(r'^$', views.HomePageView.as_view()),
#]


#from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    #path('', views.index, name='index'),
    path('', views.HomePageView.as_view()),
    path('index', views.HomePageView.as_view()),
    path('map', views.MapView.as_view()),
    path('query', views.queryView),
    path('cursus', views.cursusView),
    #path('exemple', views.post_exemple),
    #path('result', views.result),
]
