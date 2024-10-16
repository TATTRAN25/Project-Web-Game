from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "ProjectWebGame"
app_name = "Home"

urlpatterns = [
    # url home page
    path('index/',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('productDetails/<int:id>/', views.productDetails, name='productDetails'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('game/',views.game,name='game'),
    # url user
    path('login/', views.special, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('userList/', views.user_list, name='userList'),
    path('userList/create/', views.create_super_user, name='create_super_user'),
    path('userList/details/<int:pk>/', views.user_profile, name='user_profile'),
    path('userList/update/<int:pk>/', views.update_user, name='update_user'),
    path('userList/delete/<int:pk>/', views.delete_user, name='delete_user'),
    # url game
    path('gameList/', views.gameList, name='gameList'),
    path('gameList/create/', views.create_game, name='create_game'),
    path('gameList/update/<int:pk>/', views.update_game, name='update_game'),
    path('gameList/delete/<int:pk>/', views.delete_game, name='delete_game'),
    path('draft_list/', views.DraftListView, name='draft_list'),
    path('draft_list/draft_detail/<int:pk>/', views.DraftDetailView, name='draft_detail'),
    path('draft_list/publish_draft/<int:draft_id>/', views.publish_draft, name='publish_draft'),
    # url developer
    path('developer/', views.developer_list, name='developer_list'),
    path('developer/add/', views.add_developer, name='add_developer'),
    path('developer/edit/<int:developer_id>/', views.edit_developer, name='edit_developer'),
    path('developer/delete/<int:developer_id>/', views.delete_developer, name='delete_developer'),
    # url category
    path('category/', views.category_list, name='category_list'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
