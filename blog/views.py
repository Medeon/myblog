from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.
def post_list(request):
                               # if the post exists then order by publised_date
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # stuff_for_frontend = {'key': value}
    context_dictionary = {'posts': posts}
    return render(request, 'blog/post_list.html', context_dictionary)
