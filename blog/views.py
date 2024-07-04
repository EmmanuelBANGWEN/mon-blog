import json
import time
from django.shortcuts import render , get_object_or_404, redirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post
from django.views import generic
from django.core.mail import send_mail
from .models import Comment, Category, Post
from .forms import CommentForm, SearchPost, PostForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.http.response import HttpResponseRedirect, StreamingHttpResponse
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here

def post_list(request, category=None):
        
        posts = Post.published_posts.all()
        categories = Category.objects.all()
        if category:
             category = get_object_or_404(Category, slug=category)
             posts = posts.filter(category=category).order_by('published')
        paginator = Paginator(posts, 2)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger :
            posts = paginator.page(1)
        except EmptyPage :
            posts = paginator.page(paginator.num_pages)
        context = {
            
            'posts': posts,
            'page' : page,
            'categories' : categories,
            'category': category,
        }
        return render(request, 'blog/post/list.html', context)


''''class PostListView(generic.ListView):
    queryset = Post.objects.all()
    paginate_by = 2
    templates_name= 'blog/post/list.html'
    context_object_name ='posts'''

def post_detail(request,year: int, month: int, day: int, slug: str):
    post = get_object_or_404(Post, slug=slug, statut='published', published__year=year, 
                             published__month=month, published__day=day)
    comments = Comment.objects.filter(post=post.id)
    new_comment = None
    if request.method =='POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            body = comment_form.cleaned_data['body']
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
        
    return render(request, 'blog/post/detail.html',  {
                                                    'post' : post,
                                                    'comments': comments,
                                                    'new_comment' : new_comment,
                                                    'comment_form': comment_form    })


def post_search(request):
    query = None
    results = []
    search_form = SearchPost()

    if 'query' in request.GET:
        search_form = SearchPost(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            vector_search = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            query_search = SearchQuery(query)
            # results = Post.published_posts.annotate(
            #     search=vector_search, rank=SearchRank(vector_search,query_search)
            # ).filter(rank__gte=0.3).order_by('rank')
            results = Post.published_posts.annotate(
                                                    similarity=TrigramSimilarity("title", query),
                                                    ).filter(similarity__gt=0.1).order_by("-similarity")

    
    return render(request, 'blog/post/search.html', {
        'search_form': search_form,
        'query': query,
        'results': results,
    })


def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post/form.html', {'form' : form})    

def post_update(request, year: int, month: int, day: int, slug: str):
    post = get_object_or_404(Post, slug=slug, statut='published', published__year=year, 
                             published__month=month, published__day=day)
    context = {}
    if request.method == 'POST':
        form= PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/{year}/{month}/{day}/{slug}/')
    else:
        form = PostForm(instance=post)
        context['form'] = form
        context['post'] = post
    return render(request, 'blog/post/form.html', context)

def stream_view(request, post_id):
    def event_stream():
        initial_data = ""
        
        while True:
            comments = Comment.Objects.filter(post__id=post_id)\
                .values('body', 'created', 'author__username', 'post__id')
            data = json.dumps(list(comments), cls=DjangoJSONEncoder)
            if not initial_data == data:
                yield '\n'
                yield f'data :(data)'
                yield '\n\n'
                initial_data == data
            time.sleep(1)
    return StreamingHttpResponse(event_stream(content_type='text/event-stream'))

def post_share(request, post_id: int):
    post = get_object_or_404(Post, Post, pk=post_id, statut='published')
    send = False
    context = {}
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            post_url = request.bullt_absolute_uri(post.get_absolute_url())
            cl = form.cleaned_data
            subject = f'{cd["name"]} vous recomande de lire {post.title}'
            message = f'lisez {post.title} au lien {post_url} \n\n'  
                      f'(id['name'] a laissé ce comentaire comment:(cd['comments'])'
            send_mail(subject, message,cd['email'], [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        context['post'] = post
        context['form'] = form
        context['sent'] = sent
        return(request,'blog/post/share.html', context)
    