from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from accounts.forms import RegistrationForms



# Create your views here.
def login_views(request):
    if not request.user.is_authenticated:
        if request.method =='POST':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            # Redirect to a success page.
                return redirect('post_list')
            else:
                return render(request, 'registration/login.html',())

        else:
            # Return an 'invalid login' error message.
            return render(request, 'registration/login.html', {} )
    else:
        return redirect('post_list')
    

def logout_views(request):
    logout(request)
# Redirect to a success page.
    return redirect('post_list')


def register_views(request):
    if request.method == 'POST':
        user_form = RegistrationForms(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login_views')
        else:
            return render(request, 'registration/register.html', {'user_form': user_form })
    else:
        user_form = RegistrationForms()
        return render(request, 'registration/register.html', {'user_form': user_form})
    
