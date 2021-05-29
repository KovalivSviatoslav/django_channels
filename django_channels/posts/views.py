from django.views.generic import ListView, DetailView

from .models import Post

from comments.forms import CommentForm

class PostListView(ListView):

    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):

    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(self.request.POST or None)
        return context
