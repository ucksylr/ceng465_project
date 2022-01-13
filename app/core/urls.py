from django.urls import path
from . import views

urlpatterns = [
    path("", views.events, name="events"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("enroll/<int:id>", views.enroll, name="enroll"),
    path("events/add", views.add_event, name="add"),
    path("events/delete/<int:id>", views.delete_event, name="delete"),
    path("events/update/<int:id>", views.update_event, name="update"),
]
