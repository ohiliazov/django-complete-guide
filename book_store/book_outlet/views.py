from django.shortcuts import get_object_or_404, render
from django.db.models import Avg

from .models import Book


# Create your views here.
def index(request):
    books = Book.objects.all().order_by("-rating")
    total = books.count()
    avg_rating = books.aggregate(Avg("rating"))["rating__avg"]

    return render(
        request,
        "book_outlet/index.html",
        {
            "books": books,
            "total": total,
            "avg_rating": avg_rating,
        },
    )


def book_detail(request, slug: str):
    book = get_object_or_404(Book, slug=slug)
    return render(
        request,
        "book_outlet/book_detail.html",
        {
            "title": book.title,
            "author": book.author,
            "rating": book.rating,
            "is_bestseller": book.is_bestselling,
        },
    )
