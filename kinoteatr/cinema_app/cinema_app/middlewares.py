from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from datetime import timedelta, datetime
from django.utils import timezone


class TimeActionsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if 'last_request' in request.session:
            date_and_time = datetime.strptime(request.session["last_request"], "%Y-%m-%d %H:%M:%S.%f%z")
            if request.user.is_superuser is False and date_and_time + timedelta(minutes=5) < timezone.now():
                logout(request)
                return redirect('/')
            else:
                request.session['last_request'] = str(timezone.now())
