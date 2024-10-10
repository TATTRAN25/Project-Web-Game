from django.urls import path
from ProjectWebGame import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "ProjectWebGame"

urlpatterns = [
    # url home page
    path('index/',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('productDetails/<int:id>/', views.productDetails, name='productDetails'),
    path('game/',views.game,name='game'),
    # url user
    path('login/', views.special, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    # url game
    path('create_game/', views.create_game, name='create_game'),  
    path('gameList/', views.gameList, name='gameList'),  
    path('dashboard/', views.dashboard, name='dashboard'), 
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