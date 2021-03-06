"""es_policy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from es_search import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('search/', views.SearchView.as_view(), name='search'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('detail/', views.DetailView.as_view(), name='detail'),
    path('suggest/', views.SearchSuggest.as_view(), name='suggest'),
    path('hotarticle/', views.HotArticle.as_view(), name='hotarticle'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
]
