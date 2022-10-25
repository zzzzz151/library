"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from library_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('allBooks', views.allBooks, name='allBooks'),
    path('bookDisplay/<int:bookId>', views.bookDisplay, name='bookDisplay'),
    path('bookSearch/', views.bookSearch, name='bookSearch'),
    path('insert/', views.insert, name='insert'),
    path('edit/', views.edit, name='edit'),
    path('bookQuery/', views.bookQuery, name='bookQuery'),
    path('login/',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout', auth_views.LogoutView.as_view(next_page="home"), name="logout")
]
