from django.urls import path
from . import views
# from ckeditor_uploader import views as ckeditor_views

urlpatterns = [   
    # path('user_login', views.user_login, name='user_login'),
    path('upload_resume',views.upload_resume,name='upload_resume'),
    path('',views.home,name='home'),
    # path('second_views', views.second_views, name='second_views'),
    path('high_score_resumes/', views.high_score_resumes, name='high_score_resumes'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('resume/download/<int:resume_id>/', views.download_resume, name='download_resume'),
    path('resume_filter/', views.resume_filter, name='resume_filter'),
]