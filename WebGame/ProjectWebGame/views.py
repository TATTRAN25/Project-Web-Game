from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Game, Comment, Developer, Category, UserProfileInfo
from .form import CommentForm, ReplyCommentForm, UserForm, UserProfileForm, GameForm,CategoryForm,DeveloperForm
from django.core.paginator import Paginator
from django.core.mail import send_mail   
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.db.models import Count, Avg
from django.template.loader import render_to_string
import time
from django.db.models.signals import post_save
from django.dispatch import receiver

app_name = 'ProjectWebGame'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofileinfo.save()

def index(request):
    return render(request, 'Home/index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        # Kiểm tra tính hợp lệ của các biểu mẫu
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            messages.success(request, 'Đăng ký thành công!')  
            return redirect('ProjectWebGame:user_login')  

        else:
            for error in user_form.non_field_errors():
                messages.error(request, error)
            for field in user_form:
                for error in field.errors:
                    messages.error(request, error)

    else:
        user_form = UserForm() 

    return render(request, 'Home/register.html', {
        'user_form': user_form,
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

@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    logged_in_user = request.user
    users = User.objects.exclude(id=logged_in_user.id)
    return render(request, 'Users/user_list.html', {'users': users})

@login_required
def user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    comments = Comment.objects.filter(author=user)
    comments_by_game = {}
    for comment in comments:
        if comment.game not in comments_by_game:
            comments_by_game[comment.game] = []
        comments_by_game[comment.game].append(comment)

    return render(request, 'Users/user_profile.html',  {'user':user, 'comments_by_game': comments_by_game})

@user_passes_test(lambda u: u.is_superuser)
def create_super_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_superuser = True
            user.is_staff = True
            user.save()

            messages.success(request, 'Super user đã được tạo thành công.')
            return redirect('ProjectWebGame:userList')
    else:
        form = UserForm()
        return render(request, 'Users/user_form.html', {'form': form})

@login_required
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_info = UserProfileInfo.objects.get(user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES, instance=user_info)
        form.save()
        messages.success(request, 'Thông tin tài khoản đã được cập nhật thành công.')
        prevous_url = request.META.get('HTTP_REFERER').split('/')
        if (prevous_url[len(prevous_url) - 1] == "?details"):
            return redirect('ProjectWebGame:user_profile', pk=user.id)
        else:
            return redirect('ProjectWebGame:userList')
    else:
        form = UserProfileForm(instance=user_info)
        return render(request, 'Users/user_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, 'Tài khoản đã được xóa thành công.')
    return redirect('ProjectWebGame:userList')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        try:
            send_mail(
                f'Message from {name}',  
                f'From: {name}, Email: {email} \n\nMessage:\n{message}',  
                'anhtuan251104@gmail.com',  
                ['anhtuan251104@gmail.com'],  
                fail_silently=False,
            )

            send_mail(
                'Cảm ơn bạn đã góp ý!',
                'Cảm ơn bạn đã gửi ý kiến cho chúng tôi. Chúng tôi sẽ xem xét và phản hồi sớm nhất có thể.',
                'anhtuan251104@gmail.com',  
                [email],  
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('ProjectWebGame:contact')
        except Exception as e:
            messages.error(request, f'Error sending message: {e}')
            return redirect('ProjectWebGame:contact')

    return render(request, 'Home/contact.html')

def productDetails(request, id):
    game = get_object_or_404(Game, id=id)
    related_games = Game.objects.filter(category=game.category).exclude(id=game.id)[:3]
    comments = game.comments.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'You need to log in to download this game.'}, status=403)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.game = game
            comment.author = request.user
            
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)

            comment.save()
            comments = game.comments.all()

            # Trả về phản hồi JSON
            return JsonResponse({
                'author': comment.author.username,
                'text': comment.text,
                'created_date': comment.created_date.strftime("%j %B %Y"),
                'rating': comment.rating,  # Nếu có rating
            })

    else:
        form = CommentForm()

    return render(request, 'Home/productDetails.html', {
        'game': game,
        'related_games': related_games,
        'form': form,
        'comments': comments,
    })

def advertisement_page(request):
    download_link = request.GET.get('redirect')
    return render(request, 'Home/advertisement_page.html', {'download_link': download_link})

def reply_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'You need to log in to reply to comments.'}, status=403)

        form = ReplyCommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.comment = comment  # Gán bình luận cha
            reply.save()

            # Trả về phản hồi JSON
            return JsonResponse({
                'author': reply.author.username,
                'text': reply.text,
                'created_date': reply.created_date.strftime("%j %B %Y"),
            })

    return JsonResponse({'error': 'Invalid form data'}, status=400)



def game(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    sort_option = request.GET.get('sort', '')

    queryset = Game.objects.all()

    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    # Thêm các tùy chọn sắp xếp
    queryset = queryset.annotate(
        avg_rating=Avg('comments__rating'),
        comment_count=Count('comments')
    )

    if sort_option == 'high_rating':
        queryset = queryset.order_by('-avg_rating')
    elif sort_option == 'low_rating':
        queryset = queryset.order_by('avg_rating')
    elif sort_option == 'most_comments':
        queryset = queryset.order_by('-comment_count')
    elif sort_option == 'least_comments':
        queryset = queryset.order_by('comment_count')
    elif sort_option == 'latest':
        queryset = queryset.order_by('-release_date')
    elif sort_option == 'oldest':
        queryset = queryset.order_by('release_date')

    paginator = Paginator(queryset.distinct(), 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'Home/game.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_id': category_id,
        'sort_option': sort_option,
        'categories': categories,
    })

@user_passes_test(lambda u: u.is_superuser)
def gameList(request):
    games = Game.objects.all() 
    return render(request, 'Game/gameList.html', {'games': games})

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_game(request):
    form = GameForm()
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        form.save()
        messages.success(request, 'Game đã được lưu vào bản nháp!')
        return redirect('ProjectWebGame:gameList')
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
        form = GameForm(request.POST,request.FILES, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, 'Game đã được cập nhật!')
            if game.is_published == True:
                return redirect('ProjectWebGame:gameList')
            else:
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
    if game.is_published == True:
        return redirect('ProjectWebGame:gameList')
    else:
        return redirect('ProjectWebGame:draft_list')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def publish_draft(request, draft_id):
    game = get_object_or_404(Game, id=draft_id)
    game.is_published = True
    game.save()
    messages.success(request, 'Game đã được công khai!')
    return redirect('ProjectWebGame:gameList')

@user_passes_test(lambda u: u.is_superuser)
def DraftListView(request):
    drafts = Game.objects.all()
    return render(request, 'Game/draft_list.html', {'drafts': drafts})
    
@user_passes_test(lambda u: u.is_superuser)
def DraftDetailView(request, pk):
    draft = get_object_or_404(Game, pk = pk)
    return render(request, 'Game/draft_list.html', {'draft': draft})

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

def dev_category_list(request, dev_id=None, category_id=None):
    if dev_id:
        developer = get_object_or_404(Developer, id=dev_id)
        games = Game.objects.filter(developer=developer, is_published=True)
        filter_type = 'developer'
        filter_obj = developer
    elif category_id:
        category = get_object_or_404(Category, id=category_id)
        games = Game.objects.filter(category=category, is_published=True)
        filter_type = 'category'
        filter_obj = category
    else:
        games = Game.objects.filter(is_published=True)
        filter_type = None
        filter_obj = None

    paginator = Paginator(games, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    developers = Developer.objects.all()

    context = {
        'filter_type': filter_type,
        'filter_obj': filter_obj,
        'page_obj': page_obj,
        'categories': categories,
        'developers': developers,
    }
    return render(request, 'Dev_Category/dev_category_list.html', context)

# Nâng cấp vip
def upgrade_to_vip(request):
    user_profile = get_object_or_404(UserProfileInfo, user=request.user)

    # Thay đổi trạng thái VIP
    user_profile.is_vip_requested = True
    user_profile.save()

    messages.success(request, 'Your request to upgrade to VIP has been submitted. Please wait for admin approval.')
    return redirect('ProjectWebGame:user_profile', pk=request.user.id)  # Chuyển hướng về trang profile

def staff_required(user):
    return user.is_staff

@user_passes_test(staff_required)
def vip_requests(request):
    vip_requests = UserProfileInfo.objects.filter(is_vip_requested=True)
    print(vip_requests)
    return render(request, 'admin/vip_requests.html', {'vip_requests': vip_requests})

@login_required
@user_passes_test(staff_required)
def approve_vip(request, user_id):
    user_profile = UserProfileInfo.objects.get(user_id=user_id)
    user_profile.is_vip_requested = False  # Đánh dấu yêu cầu đã được xử lý
    user_profile.is_vip = True  # Đánh dấu người dùng là VIP
    user_profile.save()
    
    messages.success(request, f"{user_profile.user.username} has been upgraded to VIP.")
    return redirect('ProjectWebGame:vip_requests')