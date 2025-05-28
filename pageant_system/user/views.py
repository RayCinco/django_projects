from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'LoginPage.html')

def dashboard(request):
    return render(request, 'DashBoard.html')

def judge_dashboard(request):
    return render(request, 'JudgeDashboard.html')

def judge_profile(request):
    return render(request, 'JudgeProfile.html')

def criteria(request):
    return render(request, 'Criteria.html')

def event(request):
    return render(request, 'ManageEvent.html')

def participant_ranks(request):
    return render(request, 'ParticipantRanks.html')

def participant(request):
    return render(request, 'Participants.html')

def profile(request):
    return render(request, 'Profile.html')

def ranking(request):
    return render(request, 'Ranking.html')

def score(request):
    return render(request, 'Score.html')

def score_criteria(request):
    return render(request, 'ScoreCriteria.html')

def score_segment(request):
    return render(request, 'ScoreSegment.html')

def score_participant(request):
    return render(request, 'ScoreParticipants.html')

def segments(request):
    return render(request, 'Segments.html')


