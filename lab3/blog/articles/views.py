from django.shortcuts import render, Http404, redirect
from blog.articles.models import Article
from django.contrib.auth.models import User
from django.contrib.auth import login, logout


def archive(request):
    return render(request, "archive.html", {"posts": Article.objects.all()})


def get_article(request, id):
    try:
        post = Article.objects.filter(id=id)
        return render(request, 'article.html', {"posts": post})
    except Article.DoesNotExist:
        raise Http404


def create_post(request):
    error = []
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'text': request.POST["text"],
                'title': request.POST["title"]
            }
            if form["text"] and form["title"]:

                if len(Article.objects.filter(title=form['title'])) == 0:
                    Article.objects.create(text=form["text"],
                                           title=form["title"],
                                           author=request.user)
                    article = Article.objects.get(title=form['title'])
                    return redirect('get_article', article.id)
                else:
                    error.append("Введите уникальное название!")
                    return render(request, 'create_post.html', {'form': form, 'error': error})
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404


def create_user(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            print(request)
            form = {
                'user': request.POST['username'],
                'password': request.POST['password'],
                'email': request.POST['email']
            }
            if form['user'] and form['password'] and form['email']:
                if User.objects.filter(username=form['user']):
                    raise Http404
                else:
                    User.objects.create(username=form['user'], email=form['email'], password=form['password'])
                    return redirect('/')
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'registr.html', {'form': form})
        else:
            return render(request, 'registr.html', {})
    else:
        print(request.user)
        return redirect('/')


def dj_login(request):
    error = []
    print(request.user.is_anonymous)
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {
                'user': request.POST['username'],
                'password': request.POST['password']
            }
            someone = User.objects.get(username=form['user'])
            if someone:
                if someone.check_password(form['password']):
                    login(request, someone)
                    return redirect('/')
                else:
                    error.append("Вы ввели неправильно логин и/или пароль!")
                    return render(request, 'login.html', {'form': form, 'error': error})
            else:
                raise Http404
        else:
            return render(request, 'login.html')
    else:
        return redirect('/')


def dj_logout(request):
    if not request.user.is_anonymous:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')
