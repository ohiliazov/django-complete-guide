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
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        return stored_posts and post_id in stored_posts

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
                "saved_for_later": self.is_stored_post(request, post.id),
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
                "saved_for_later": self.is_stored_post(request, post.id),
            },
        )


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}
        if not stored_posts:
            context["posts"] = []
            context["has_posts"] = False
        else:
            context["posts"] = Post.objects.filter(id__in=stored_posts)
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts", [])
        post_id = int(request.POST["post_id"])

        if post_id in stored_posts:
            stored_posts.remove(post_id)
        else:
            stored_posts.append(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
