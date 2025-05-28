from . import views
from django.urls import path


urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='organizer-dashboard'),
    path('judge/dashboard/', views.judge_dashboard, name='judge-dashboard'),
    path('judge/profile/', views.judge_profile, name='judge-profile'),

    path('criteria/', views.criteria, name='criteria'),
    path('manage/event/', views.event, name='manage-event'),
    path('participant/ranks/', views.participant_ranks, name='participant-ranks'),
    path('participants/', views.participant, name='participants'),

    path('profile/', views.profile, name='organizer-profile'),
    path('ranking/', views.ranking, name='organizer-ranking'),
    path('score/', views.score, name='organizer-score'),
    path('score/criteria/', views.score_criteria, name='organizer-score-criteria'),
    path('score/segment/', views.score_segment, name='organizer-score-segment'),
    path('score/participant/', views.score_participant, name='organizer-score-participant'),
    path('segments/', views.segments, name='organizer-segments'),
]