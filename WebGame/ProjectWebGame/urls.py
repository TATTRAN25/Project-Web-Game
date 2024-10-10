from django.urls import path
from ProjectWebGame import views

app_name = "ProjectWebGame"

urlpatterns = [
    path('index/',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('productDetails/',views.productDetails,name='productDetails'),
    path('game/',views.game,name='game'),
    path('login/', views.special, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('gameList/game_form/', views.game_form, name='game_form'),
    path('add_review/<int:game_id>/', views.add_review, name='add_review'),  
    path('publish_draft/<int:draft_id>/', views.publish_draft, name='publish_draft'),   
    path('gameList/', views.gameList, name='gameList'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('draft_list/', views.DraftListView, name='draft_list'),
]