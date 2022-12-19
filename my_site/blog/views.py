from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .forms import CommentForm
from .models import Post


class StartingPageView(ListView):
    context_object_name = "posts"
    model = Post
    ordering = ["-date"]
    template_name = "blog/index.html"

    def get_queryset(self):
        return super().get_queryset()[:3]


class AllPostsView(ListView):
    context_object_name = "posts"
    model = Post
    template_name = "blog/all-posts.html"
    ordering = ["-date"]


class SinglePostView(View):
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        return render(
            request,
            "blog/post-detail.html",
            {
                "post": post,
                "post_tags": post.tags.all(),
                "comments": post.comments.order_by("-id").all(),
                "comment_form": CommentForm(),
            },
        )

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(
                reverse(
                    "post-detail-page",
                    args=[slug],
                )
            )

        return render(
            request,
            "blog/post-detail.html",
            {
                "post": post,
                "post_tags": post.tags.all(),
                "comments": post.comments.order_by("-id").all(),
                "comment_form": comment_form,
            },
        )


class ReadLaterView(View):
    def post(self, request):
        stored_posts = request.session.get("stored_posts", [])
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)

        return HttpResponseRedirect("/")
