from django.urls import path
from .views import ResumeUploadView, ResumeQueryView, ResumeSearchView, ResumeListView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('query/', ResumeQueryView.as_view(), name='resume-query'),
    path('search/', ResumeSearchView.as_view(), name='resume-search'),
    path('candidates/', ResumeListView.as_view(), name='resume-list'), 
]
