from django.urls import path
from . import views

urlpatterns = [
    path("create-course/", views.create_course),
    path("course/<int:course_id>/create-standard/", views.create_standard)
]