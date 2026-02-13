from .models import AppUser

def app_user(request):
    u = None
    if request.session.get('user_id'):
        try:
            u = AppUser.objects.filter(id=request.session['user_id']).first()
        except Exception:
            u = None
    return {
        'app_user': u,
        'app_role': request.session.get('role')
    }
