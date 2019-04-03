from django.contrib.auth.decorators import login_required
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

@login_required(login_url='/accounts/login')
def post_new(request):
    # By submitting the form (equal to Post request) run:
    if request.method == 'POST':
        # fill out the form based on the received information from POST
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # the poster = the current ,logged in, user
            post.author = request.user
            post.save()
            # show result immedeatly after saving the form
            return redirect('post_detail', pk=post.pk)
    # Runs the form by default as a Get request:
    else:
        form = PostForm()
        context_dictionary = {'form': form}
    return render(request, 'blog/post_edit.html', context_dictionary)

@login_required(login_url='/accounts/login')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':

        # updating an existing form
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        context_dictionary = {'form': form, 'post': post}
    return render(request, 'blog/post_edit.html', context_dictionary)

@login_required(login_url='/accounts/login')
def post_draft_list(request):
    # show all of the drafts in decending order:
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    context_dictionary = {'posts': posts}
    return render(request, 'blog/post_draft_list.html', context_dictionary)

@login_required(login_url='/accounts/login')
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)