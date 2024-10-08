from django.shortcuts import render, redirect
from .form import UserForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Game, Review

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password']) 
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user 
            if 'user_pic' in request.FILES:
                profile.user_pic = request.FILES['user_pic']
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

    return render(request, 'ProjectWebGame/registration.html', {
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
    if request.user.is_authenticated:
        messages.info(request, 'Bạn đã đăng nhập rồi!')
        return HttpResponseRedirect(reverse('RegistrationLogin:index'))

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

@login_required
def create_game(request):
    if request.method == 'POST':
        # Logic để tạo game
        game = Game(
            name=request.POST['name'],
            description=request.POST['description'],
            developer=request.user, 
            is_published=False
        )
        game.save()
        messages.success(request, 'Game đã được lưu vào bản nháp!')
        return redirect('game_list')

@login_required
def add_review(request, game_id):
    game = Game.objects.get(id=game_id)
    if request.method == 'POST':
        review = Review(
            user=request.user,
            game=game,
            content=request.POST['content'],
            rating=request.POST['rating'],
            is_published=False 
        )
        review.save()
        messages.success(request, 'Bình luận đã được lưu vào bản nháp!')
        return redirect('game_detail', game_id=game.id)

@login_required
def publish_draft(request, draft_id, is_game=True):
    if is_game:
        game = Game.objects.get(id=draft_id)
        game.is_published = True
        game.save()
        messages.success(request, 'Game đã được công khai!')
    else:
        review = Review.objects.get(id=draft_id)
        review.is_published = True
        review.save()
        messages.success(request, 'Bình luận đã được công khai!')
    return redirect('dashboard') 