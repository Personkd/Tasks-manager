import django.contrib.auth.mixins
from django.shortcuts import redirect
class IsAuthenticated(django.contrib.auth.mixins.AccessMixin):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated != True:
            return redirect("/")
        return super().dispatch(request,*args,**kwargs)
