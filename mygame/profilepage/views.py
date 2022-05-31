from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from profilepage.models import Games


# Create your views here.

@login_required
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        games = Games.objects.filter(player=user)
        # player = games.player.exclude(User)
        # winner = games.winner
        return render(request, 'profilepage/profile.html', {
            'games': games,
        })

# data = Students.objects.all()
#
# stu = {
#     "student_number": data
# }
#
#
# return render_to_response("login/profile.html", stu)
