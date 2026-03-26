from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>', views.ArticlesDetailsView.as_view(), name='articles_detail'),
    path('add_article', views.add_article, name='article_add'),
    path('like/<int:pk>/', views.like_article, name='like_article'),
    path('comment/<int:pk>/', views.add_comment, name='comment_article'),
    path('<int:pk>/update', views.ArticleUpdateView.as_view(), name='update_article'),
    path('<int:pk>/delete', views.ArticleDeleteView.as_view(), name='delete_article'),
]