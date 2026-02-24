from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns=[
    path("", UserView.as_view()),
    path("subject/", Subject.as_view()),
    path("course/", Course.as_view()),
    path("batch/", Batch.as_view()),
    path("enrollment/", Enrollment.as_view()),
    path("mark/", Mark.as_view()),
    path("login/", LoginView.as_view()),

]