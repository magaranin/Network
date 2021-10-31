
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_new_post", views.create_new_post, name="create_new_post"),
    path("profile_page/<int:profile_owner_id>", views.profile_page, name="profile_page"),
    path("update_follows/<int:profile_owner_id>", views.update_follows, name="update_follows"),
    path("following", views.following, name="following"),
    path("posts/<int:post_id>", views.update_post, name ="update_post"),
    path("posts/<int:post_id>/like_unlike", views.like_unlike, name ="like_unlike")

]
