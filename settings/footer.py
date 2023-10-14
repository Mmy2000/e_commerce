from .models import Info

def myfooter(request):
    myfooter = Info.objects.last()
    return{'myfooter':myfooter}