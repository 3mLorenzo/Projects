
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("new_post/", views.new_post, name="new_post"),
    path("profile_page/<int:user_id>", views.profile_page, name="profile_page"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("r_like/<int:post_id>", views.r_like, name="r_like"),
    path("a_like/<int:post_id>", views.a_like, name="a_like"),
]
