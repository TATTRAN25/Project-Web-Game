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
<<<<<<< HEAD
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
=======
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
>>>>>>> django/3-TAT
