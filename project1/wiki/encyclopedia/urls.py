from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path('new_page/', views.new_page, name="new_page"),
    path('random_page/', views.random_page, name="random_page"),
    path('search/', views.search, name="search"),
    path('edit/', views.edit, name="edit"),
    path('editsave', views.editsave, name="editsave")
]
