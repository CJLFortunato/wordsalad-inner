from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .admin import UserCreationForm
from .models import User
from .forms import UpdateUserInfo

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("projects:dashboard")
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {
        "form": form
    })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("projects:dashboard")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {
        "form": form
    })

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('/')

@login_required(login_url="/users/login")
def manage_view(request):
    user = User.objects.get(id=request.user.id)
    print(user.__dict__)
    info_form = UpdateUserInfo(data={
            "info_email": user.email,
            "info_timezone": user.timezone
        }, prefix="info")
        # print(info_form["email"].data)
    password_form = PasswordChangeForm(user=user)

    if request.method == "POST":
        print(request.POST)
        if 'info_email' in request.POST:
            info_form = UpdateUserInfo(request.POST, prefix="info")
            # if request.POST["email"] == user.email:
            #     change_email = True

            # if change_email:
            user.email = info_form["email"].data
            user.timezone = info_form["timezone"].data

            # form.save(commit=False)
            # if form.password:
            #     user.password = form.password
            # print(user.__dict__)
            user.save()
            return redirect('users:manage')
    else:
        print(user.email)
        info_form = UpdateUserInfo(data={
            "info_email": user.email,
            "info_timezone": user.timezone
        }, prefix="info")
        # print(info_form["email"].data)
        password_form = PasswordChangeForm(user=user)
    print(info_form)
    return render(request, 'users/manage.html', {
         "info_form": info_form,
         "password_form": password_form
     })