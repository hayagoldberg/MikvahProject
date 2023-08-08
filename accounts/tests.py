from django.test import TestCase

# Create your tests here.

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # connecter l'utilisateur et rediriger
            return redirect('website:pro_page')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {"form": form})