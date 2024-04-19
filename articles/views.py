from django.shortcuts import render,redirect
from .models import Article
from .forms import ArticleForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST


# Create your views here.
def index(request):
    return render(request, "articles/index.html")

def articles(request):
    articles = Article.objects.all().order_by("-pk")
    context={
        "articles":articles
    }
    return render(request, "articles/articles.html", context)


def article_detail(request,pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comment=article.comments.all().order_by("-pk")
    context = {
        "article":article,
        "comment_form":comment_form,
        "commensts": comment,
    }
    return render(request, "articles/article_detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("articles:article_detail", article.id)
    else:
        form= ArticleForm()

    context = {"form": form}
    return render(request, "articles/create.html", context)



def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect("articles:article_detail", article.pk)
    else:
        form = ArticleForm(instance=article)

    context = {
        "form": form,
        "article": article,
    }
    return render(request, "articles/update.html", context)


@require_POST
def delete(request, pk):
    if request.method =="POST":
        article = Article.objects.get(pk=pk)
        article.delete()
        return redirect("articles:articles")
    return redirect("articles:article_detail",pk)



@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=pk)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect("articles:articles")
    return redirect("accounts:login")


@require_POST
def comment_create(request, pk):
    article = Article.objects.get(pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comments = form.save(commit=False)
        comments.article_id=pk
        comments.save()
        return redirect("articles:article_detail",pk)





def data_throw(request):
    return render(request,"articles/data_throw.html")

def data_catch(request):
    message = request.GET.get("message")
    context = {"message" : message}
    return render(request,"articles/data_catch.html", context)

