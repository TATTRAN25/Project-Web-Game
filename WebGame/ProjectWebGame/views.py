from django.shortcuts import render, redirect
from .form import UserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'registration/index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Sửa ở đây
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user 
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save() 

            messages.success(request, 'Đăng ký thành công!') 
            return redirect('RegistrationLogin:index') 

        else:
            for error in user_form.non_field_errors():
                messages.error(request, error)
            for field in user_form:
                for error in field.errors:
                    messages.error(request, error)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/registration.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def special(request):
    return HttpResponse("Bạn đang đăng nhập!")

def user_logout(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công!')
    return HttpResponseRedirect(reverse('RegistrationLogin:index'))

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công!')
                return HttpResponseRedirect(reverse('RegistrationLogin:index'))
            else:
                messages.error(request, 'Tài khoản của bạn đã bị vô hiệu hóa.')
                return HttpResponse('Account not activated')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác.')
            return HttpResponse('Invalid login details supplied!')

    return render(request, 'registration/login.html')

def contact(request):
    return render(request, 'contact.html')

def productDetails(request):
    return render(request, 'productDetails.html')

def shop(request):
    return render(request, 'shop.html')