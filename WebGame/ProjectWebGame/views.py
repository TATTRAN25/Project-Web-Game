from .form import UserForm, UserProfileForm, GameForm,DeveloperForm, CategoryForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Game, Review, Developer, Category

def index(request):
    return render(request, 'Home/index.html')

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
            return redirect('ProjectWebGame:user_login')  

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

    return render(request, 'Home/register.html', {
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
    
    return render(request, 'Home/login.html')

def contact(request):
    return render(request, 'Home/contact.html')

def productDetails(request):
    return render(request, 'Home/productDetails.html')

def game(request):
    return render(request, 'Home/game.html')

@login_required
def game_form(request):
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST)
    else:
        form = GameForm()
    return render(request, 'Game/game_form.html', {'form': form})

def gameList(request):
    games = Game.objects.all() 
    return render(request, 'Game/gameList.html', {'games': games})

def dashboard(request):
    return render(request, 'Game/dashboard.html')

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
        return render(request, 'Game/create_game_form.html')

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
        return redirect('Game/game_detail', game_id=game.id)

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

# Crud Dev and Category
@login_required
@user_passes_test(lambda u: u.is_superuser)
def developer_list(request):
    developers = Developer.objects.all()
    return render(request, 'Dev_Category/developer_list.html', {'developers': developers})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'Dev_Category/category_list.html', {'categories': categories})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_developer(request):
    if request.method == 'POST':
        form = DeveloperForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Developer added successfully!')
            return redirect('ProjectWebGame:developer_list')
    else:
        form = DeveloperForm()
    return render(request, 'Dev_Category/developer_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_developer(request, developer_id):
    developer = get_object_or_404(Developer, id=developer_id)
    if request.method == 'POST':
        form = DeveloperForm(request.POST, request.FILES, instance=developer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Developer updated successfully!')
            return redirect('ProjectWebGame:developer_list')
    else:
        form = DeveloperForm(instance=developer)
    return render(request, 'Dev_Category/developer_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_developer(request, developer_id):
    developer = get_object_or_404(Developer, id=developer_id)
    if request.method == 'POST':
        developer.delete()
        messages.success(request, 'Developer deleted successfully!')
        return redirect('ProjectWebGame:developer_list')
    return render(request, 'Dev_Category/confirm_delete.html', {'object': developer})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('ProjectWebGame:category_list')
    else:
        form = CategoryForm()
    return render(request, 'Dev_Category/category_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('ProjectWebGame:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'Dev_Category/category_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('ProjectWebGame:category_list')
    return render(request, 'Dev_Category/confirm_delete.html', {'object': category})