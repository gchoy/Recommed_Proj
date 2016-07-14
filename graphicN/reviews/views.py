from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
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



def add_review(request, comic_id):
    comic = get_object_or_404(Comic, pk=comic_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
       rating = form.cleaned_data['rating']
       comment = form.cleaned_data['comment']
       user_name = form.cleaned_data['user_name']
       review = Review()
       review.comic = comic
       review.user_name = user_name
       review.rating = rating
       review.comment = comment
       review.pub_date = datetime.datetime.now()
       review.save()
       return HttpResponseRedirect(reverse('reviews:comic_detail', args=(comic.id,)))
    return render(request, 'reviews/comic_detail.html', {'comic': comic, 'form': form})
