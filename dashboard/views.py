from django.shortcuts import render, redirect


# Create your views here.
def home_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("signin_view")
    template_name = "dashboard.html"
    context = {}

    return render(request, template_name, context)
