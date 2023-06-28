from django.urls import path
from . import views

urlpatterns = [
    path("create-course/", views.create_course),
    path("course/<int:course_id>/create-standard/", views.create_standard),
    path("", views.dashboard),
    path("course/<int:course_id>/", views.course),
    path("course/<int:course_id>/add-question", views.add_question_view),
    path("course/<int:course_id>/view-questions/s/<int:standard_id>/", views.view_questions_by_standard)
]