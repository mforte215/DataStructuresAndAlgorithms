from audioop import reverse
from .forms import UserCreateForm
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import Article, Comment
from django.contrib.auth import authenticate, login

def IndexView(request):
    article_list = get_list_or_404(Article)
    return render(request, 'app/index.html', {'articles': article_list})

def LoginView(request):
    if request.method == 'GET':
        context = {}
        if request.user.is_authenticated:
            return render(request, 'app/index.html', context)
        else:
            return render(request, 'registration/login.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            context = {'error_message', 'Sorry, Username/Password Not Found'}
            return render(request, 'registration/login.html', context)

def ArticleDetailView(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'app/article-detail.html', {'article': article})

class SignUpForm(generic.CreateView):
    form_class= UserCreateForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


def DeleteCommentConfirmView(request, pk):
    if request.method == 'GET':
        context = {}
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=pk)
            if comment is not None:
                if request.user == comment.user:
                    return render(request, 'app/delete-comment-confirm.html', {'comment': comment })
                else:
                    return HttpResponseRedirect(reverse_lazy('index'))
            else:
                return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return HttpResponseRedirect(reverse_lazy('login'))
    elif request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comment.objects.get(pk=pk)
            if request.user == comment.user:
                comment.delete()
                return HttpResponseRedirect(reverse_lazy('profile'))
            else:
                return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return HttpResponseRedirect(reverse_lazy('login'))

