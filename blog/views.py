from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post

# Create your views here.
def post_list(request):
                               # if the post exists then order by publised_date
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # stuff_for_frontend = {'key': value}
    context_dictionary = {'posts': posts}
    return render(request, 'blog/post_list.html', context_dictionary)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context_dictionary = {'post': post}
    return render(request, 'blog/post_detail.html', context_dictionary)

def post_new(request):
    # By submitting the form (equal to Post request) run:
    if request.method == 'POST':
        # fill out the form based on the received information from POST
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # the publisher = the current ,logged in, user
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # show result immedeatly after saving the form
            return redirect('post_detail', pk=post.pk)
    # Runs the form by default as a Get request:
    else:
        form = PostForm()
        context_dictionary = {'form': form}
    return render(request, 'blog/post_edit.html', context_dictionary)

