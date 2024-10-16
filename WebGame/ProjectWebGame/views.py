from .form import UserForm, UserProfileForm, GameForm,CategoryForm,DeveloperForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Game, Draft, Comment, Developer, Category
from .form import CommentForm, ReplyCommentForm
from .models import Game, Draft, Post, Comment, Developer, Category
from .form import CommentForm
from django.views.generic import (TemplateView, ListView, DeleteView, CreateView, UpdateView, UpdateView, DeleteView, DetailView)
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.paginator import Paginator

app_name = 'ProjectWebGame'

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

def productDetails(request, id):
    game = get_object_or_404(Game, id=id)
    related_games = Game.objects.filter(category=game.category).exclude(id=game.id)[:3]
    comments = game.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to download this game.")
            return redirect('login')
        
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.game = game
            comment.author = request.user
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)

            comment.save()
            #print(f"Comment saved: {comment.text} with rating: {comment.rating}")
            messages.success(request, "Your comment has been added.")
            comments = game.comments.all()
            return redirect('Home:productDetails', id=game.id)
    else:
        form = CommentForm()

    return render(request, 'Home/productDetails.html', {'game': game, 'related_games': related_games, 'form': form, 'comments': comments,})

def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to reply to comments.")
            return redirect('login')

        form = ReplyCommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.comment = comment  # Gán bình luận cha
            reply.save()
            #print(f"Comment ID: {comment_id}, Game ID: {comment.game.id}")
            messages.success(request, "Your reply has been added.")
            return redirect('Home:productDetails', id=comment.game.id)

    # Xử lý trường hợp GET hoặc lỗi form
    form = CommentForm()
    return render(request, 'Home/productDetails.html', {
        'form': form,
        'comments': Comment.objects.filter(game=comment.game),
    })



def game(request):
    search_query = request.GET.get('search', '')  # Lấy tham số tìm kiếm
    category_id = request.GET.get('category')  # Lấy tham số category

    if search_query:
        game_list = Game.objects.filter(name__icontains=search_query)
    elif category_id:
        game_list = Game.objects.filter(category_id=category_id)  # Lọc theo category
    else:
        game_list = Game.objects.all()  # Lấy tất cả nếu không có tìm kiếm hoặc category

    paginator = Paginator(game_list, 4) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all() 

    return render(request, 'Home/game.html', {
        'page_obj': page_obj, 
        'search_query': search_query,
        'categories': categories    
    })

@user_passes_test(lambda u: u.is_superuser)
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
    form = GameForm()
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
        form = GameForm()
        return render(request, 'Game/game_form.html', {'form': form})
    
@login_required
def publish_draft(request, draft_id):
    game = get_object_or_404(Game, id=draft_id)
    game.is_published = True
    game.save()
    messages.success(request, 'Game đã được công khai!')
    return redirect('ProjectWebGame:gameList')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game đã được cập nhật!')
            return redirect('ProjectWebGame:draft_list')
    else:
        form = GameForm(instance=game)
        return render(request, 'Game/game_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    game.delete()
    messages.success(request, 'Game đã xóa thành công!')
    return redirect('ProjectWebGame:gameList')

@user_passes_test(lambda u: u.is_superuser)
def DraftListView(request):
    drafts = Game.objects.all()
    return render(request, 'Game/draft_list.html', {'drafts': drafts})

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'Home/gameList.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('ProjectWebGame:post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('ProjectWebGame:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'ProjectWebGame/comment_form.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('ProjectWebGame:post_detail', pk=comment.post.pk)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Kiểm tra xem người dùng có quyền xóa không
    if request.user.is_staff or request.user == comment.author:
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this comment.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

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
