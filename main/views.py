from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, DeleteView
from django.db.models import Q
from unicodedata import category

from main.forms import ArticlesForm
from main.models import Articles, Comment
from users.forms import UserRegisterForm


def index(request):
    articles = Articles.objects.all()
    category_filter = request.GET.get('category')
    search_query = request.GET.get('q')

    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    if category_filter:
        articles = articles.filter(category=category_filter)

    return render(request, 'main/index.html', {'articles': articles})

class ArticlesDetailsView(DetailView):
    model = Articles
    template_name = 'main/articles_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        session_key = f'viewed_article_{obj.id}'

        if not self.request.session.get(session_key, False):
            obj.views += 1
            obj.save(update_fields=['views'])

            self.request.session[session_key] = True

        return obj

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Articles
    template_name = 'main/update_delete_article.html'
    form_class = ArticlesForm

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Articles
    success_url = '/'
    template_name = 'main/update_delete_article.html'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


@login_required(login_url='login')
def add_article(request):
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('index')
        else:
            errors = form.errors


    form = ArticlesForm()
    return render(request, 'main/add_article.html', {'form': form})


@login_required(login_url='login')
def like_article(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You need to log in'}, status=401)

    article = get_object_or_404(Articles, id=pk)

    liked = False

    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True

    return JsonResponse({'total_likes': article.total_likes(), 'liked': liked})


@login_required(login_url='login')
def add_comment(request, pk):
    article = get_object_or_404(Articles, id=pk)

    if request.method == 'POST':
        text = request.POST.get('content')

        if text:
            Comment.objects.create(
                article=article,
                author=request.user,
                content=text
            )

    return redirect('articles_detail', pk=pk)



