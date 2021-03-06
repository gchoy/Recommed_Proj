from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .suggestions import update_clusters

from .models import Review, Comic
from .forms import ReviewForm

import datetime


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def comic_list(request):
    comic_list = Comic.objects.order_by('-name')
    context = {'comic_list':comic_list}
    return render(request, 'reviews/comic_list.html', context)


def comic_detail(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    form = ReviewForm()
    return render(request, 'reviews/comic_detail.html', {'comic': comic, 'form': form})


@login_required
def add_review(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
       rating = form.cleaned_data['rating']
       comment = form.cleaned_data['comment']
       user_name = request.user.username
       review = Review()
       review.comic = comic
       review.user_name = user_name
       review.rating = rating
       review.comment = comment
       review.pub_date = datetime.datetime.now()
       review.save()
       update_clusters()
       return HttpResponseRedirect(reverse('reviews:comic_detail', args=(comic.id,)))
    return render(request, 'reviews/comic_detail.html', {'comic': comic, 'form': form})

def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list':latest_review_list, 'username':username}
    return render(request, 'reviews/user_review_list.html', context)

@login_required
def user_recommendation_list(request):
    # get this user reviews
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('comic')
    # from the reviews, get a set of wine IDs
    user_reviews_comic_ids = set(map(lambda x: x.comic.id, user_reviews))

    try:
        user_cluster_name = \
           User.objects.get(username=request.user.username).cluster_set.first().name
    except:
        update_clusters()
        user_cluster_name = \
           User.objects.get(username=request.user.username).cluster_set.first().name

    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users \
            .exclude(username=request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
            .exclude(comic__id__in=user_reviews_comic_ids)
    other_users_reviews_comic_ids = set(map(lambda x: x.comic.id, other_users_reviews))

    comic_list = sorted(
        list(Comic.objects.filter(id__in=other_users_reviews_comic_ids)),
        key=lambda x: x.average_rating,
        reverse=True
    )

    return render(
        request,
        'reviews/user_recommendation_list.html',
        {'username': request.user.username,'comic_list': comic_list}
    )

    #comic_list = Comic.objects.exclude(id__in=user_reviews_comic_ids)
    #return render(request, 'reviews/user_recommendation_list.html', {'username':request.user.username})
