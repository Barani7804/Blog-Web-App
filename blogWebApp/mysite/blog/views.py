
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm


def post_list(request):
    posts = Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    #list of actve comments for this post
    comments = post.comments.filter(active=True)
    #form for users comment
    form = CommentForm()


    return render(
        request,
        'blog/post/detail.html',
        {
         'post': post,
         'comments': comments,
         'form': form
         }
        
        
    )



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        }
    )