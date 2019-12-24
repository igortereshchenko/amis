from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from vcs import views

urlpatterns = [
    path('login/', login_required(views.StudentLoginView.as_view()), name='student_login'),
    path('lectures/', login_required(views.LectureList.as_view()), name='lecture_list'),
    path('lectures/<int:pk>/', login_required(views.LectureDetail.as_view()), name='lecture_detail'),
    path('packs-list/', login_required(views.LecturePackList.as_view()), name='lecture_pack_list'),
    path('packs/<str:pk>/', login_required(views.LecturePackDetail.as_view()), name='lecture_pack_detail'),
    path('predict-score/<str:lecture_id>/', login_required(views.PredictScore.as_view()), name='predict_score'),
]
