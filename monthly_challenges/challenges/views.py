from django.shortcuts import render
from django.http import (
    HttpRequest,
    Http404,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.urls import reverse

monthly_challenges = {
    "january": "Eat no meat for the entire month!",
    "february": "Walk for at least 20 minutes every day!",
    "march": "Learn Django for at least 20 minutes every day!",
    "april": "Eat no meat for the entire month!",
    "may": "Walk for at least 20 minutes every day!",
    "june": "Learn Django for at least 20 minutes every day!",
    "july": "Eat no meat for the entire month!",
    "august": "Walk for at least 20 minutes every day!",
    "september": "Learn Django for at least 20 minutes every day!",
    "october": "Eat no meat for the entire month!",
    "november": "Walk for at least 20 minutes every day!",
    "december": None,
}


def index(request: HttpRequest):
    return render(
        request, "challenges/index.html", {"months": monthly_challenges.keys()}
    )


def monthly_challenge_by_number(request: HttpRequest, month: int):
    months = list(monthly_challenges.keys())

    if not 0 < month <= len(months):
        return HttpResponseNotFound("Invalid month!")

    redirect_month = months[month - 1]
    redirect_url = reverse("month-challenge", args=[redirect_month])
    return HttpResponseRedirect(redirect_url)


def monthly_challenge(request: HttpRequest, month: str):
    try:
        challenge_text = monthly_challenges[month]
    except KeyError:
        raise Http404()

    return render(
        request,
        "challenges/challenge.html",
        {
            "month_name": month,
            "challenge_text": challenge_text,
        },
    )
