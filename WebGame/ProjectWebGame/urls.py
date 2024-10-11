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
    path('create_game/', views.create_game, name='create_game'),  
    path('add_review/<int:game_id>/', views.add_review, name='add_review'),  
    path('publish_draft/<int:draft_id>/', views.publish_draft, name='publish_draft'),   
    path('gamelist/', views.game, name='gameList'),  
    path('dashboard/', views.dashboard, name='dashboard'),
    #path('draft_list/', views.DraftListView, name='draft_list'),

    path('post_list/', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

]