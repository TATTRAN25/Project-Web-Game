from django.shortcuts import render, redirect,get_object_or_404
from .form import UserForm, UserProfileForm, GameForm
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Game, Review

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST, files=request.FILES)

        # Kiểm tra tính hợp lệ của các biểu mẫu
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user  
            profile.save()  

            messages.success(request, 'Đăng ký thành công!')  
            return redirect('ProjectWebGame:index')  

        # Nếu có lỗi, hiển thị thông báo lỗi
        else:
            for error in user_form.non_field_errors():
                messages.error(request, error)
            for field in user_form:
                for error in field.errors:
                    messages.error(request, error)
            for field in profile_form:
                for error in field.errors:
                    messages.error(request, error)

    else:
        user_form = UserForm() 
        profile_form = UserProfileForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def special(request):
    return HttpResponse("Bạn đang đăng nhập!")

def user_logout(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công!')
    return HttpResponseRedirect(reverse('ProjectWebGame:index'))

def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, 'Bạn đã đăng nhập rồi!')
        return redirect('ProjectWebGame:index')  
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('ProjectWebGame:index') 
            else:
                messages.error(request, 'Tài khoản của bạn đã bị vô hiệu hóa.')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không chính xác.')
    
    return render(request, 'login.html')

def contact(request):
    return render(request, 'contact.html')

def productDetails(request):
    return render(request, 'productDetails.html')

def game(request):
    return render(request, 'game.html')

@login_required
def game_form(request):
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST)
    else:
        form = GameForm()
    return render(request, 'game_form.html', {'form': form})

def gameList(request):
    games = Game.objects.all() 
    return render(request, 'gameList.html', {'games': games})

def dashboard(request):
    return render(request, 'dashboard.html')

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_game(request):
    if request.method == 'POST':
        game = Game(
            name=request.POST['name'],
            description=request.POST['description'],
            developer=request.user,
            is_published=False  # Đặt chế độ nháp
        )
        game.save()
        messages.success(request, 'Game đã được lưu vào bản nháp!')
        return redirect('ProjectWebGame:game_list') 
    else:
        return render(request, 'create_game_form.html')

@login_required
def add_review(request, game_id):
    game = get_object_or_404(Game, id=game_id)
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
        game = get_object_or_404(Game, id=draft_id)
        game.is_published = True
        game.save()
        messages.success(request, 'Game đã được công khai!')
    else:
        review = get_object_or_404(Review, id=draft_id)
        review.is_published = True
        review.save()
        messages.success(request, 'Bình luận đã được công khai!')
    return redirect('dashboard')