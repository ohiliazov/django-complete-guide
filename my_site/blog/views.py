from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post

posts = []


def get_date(post: dict):
    return post.get("date")


def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    return render(
        request,
        "blog/index.html",
        context={"posts": latest_posts},
    )


class StartPageView(ListView):
    template_name = "blog/all-posts.html"
    model = Post

    def get_ordering(self):
        pass


def posts_page(request):
    posts = Post.objects.all().order_by("-date")
    return render(
        request,
        "blog/all-posts.html",
        context={"posts": posts},
    )


def post_detail(request, slug: str):
    post = get_object_or_404(Post, slug=slug)

    return render(
        request,
        "blog/post-detail.html",
        context={
            "post": post,
            "post_tags": post.tags.all(),
        },
    )
