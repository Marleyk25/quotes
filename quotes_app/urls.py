from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path("login", views.login),
    path('quote', views.quote),
    path('addquote', views.addquote),
    path('user/<userID>', views.showuser),
    path('editquote/<quoteid>', views.editquote),
    path('quote/<quoteID>', views.showquote),
    path('favquote/<qobjID>', views.favquote),
    path('removefav/<favqobjID>', views.removefav),
    path('logout', views.logout),
]
