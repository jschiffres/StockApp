"""stockbrokerage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from stockapp import views


urlpatterns = [
    path('admin/', admin.site.urls),

    #HOME
    path('', views.home, name="home"),

    #AUTH
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    #PORTFOLIOS
    path('createportfolio/', views.createportfolio, name='createportfolio'),
    path('myportfolios/', views.myportfolios, name='myportfolios'),
    path('viewportfolio/<int:portfolio_pk>', views.viewportfolio, name='viewportfolio'),
    path('editportfolio/<int:portfolio_pk>', views.editportfolio, name='editportfolio'),
    path('portfolio/<int:portfolio_pk>/delete', views.deleteportfolio, name='deleteportfolio'),
    path('powerbitest/', views.powerbitest, name='powerbitest'),
    path('hannah/', views.hannah, name='hannah'),
    
    #STOCKS
    path('stock/<str:stock_ticker>', views.stockpage, name='stockpage'),
]
