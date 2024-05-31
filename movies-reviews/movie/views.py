from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Movie, Review

from .forms import ReviewForm

from . forms import MovieForm

def home(request):
    """landing page"""
    search_term = request.GET.get('searchCategory', '')

    if search_term:
        movies = Movie.objects.filter(
            category__icontains=search_term).order_by('category')
    else:
        movies = Movie.objects.all().order_by('category')

    return render(request, 'home.html', {
        'searchTerm': search_term,
        'movies': movies
    })


def detail(request, movie_id):
    """returns detail page for the selected movie"""
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)

    return render(request, 'detail.html', {
        'movie': movie,
        'reviews': reviews
    })


def about(request):
    return HttpResponse('<h1>Welcome to the about page</h1>')


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


@login_required
def create_review(request, movie_id):
    """creates a new review"""
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'GET':
        return render(request, 'create_review.html', {
            'form': ReviewForm(),
            'movie': movie
        })
    else:
        try:
            form = ReviewForm(request.POST)
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.movie = movie
            new_review.save()
            return redirect('movie:detail', movie_id=new_review.movie.id)
        except ValueError:
            return render(request, 'create_review.html', {
                'form': ReviewForm(),
                'error': 'Bad data passed in'
            })


@login_required
def update_review(request, review_id):
    """update a movie review"""

    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method == 'GET':
        form = ReviewForm(instance=review)

        return render(request, 'update_review.html', {
            'review': review,
            'form': form
        })
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)

        except ValueError:
            return render(request, 'update_review.html', {
                'form': form,
                'error': 'Bad data in form'
            })


@login_required
def delete_review(request, review_id):
    """deletes a review"""

    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()

    return redirect('detail', review.movie.id)


def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        year = request.POST.get('year')
        actors = request.POST.get('actors')
        release_date = request.POST.get('release_date')
        category = request.POST.get('category')
        url = request.POST.get('url')
        if title and description and image and year and release_date and actors and category:
            movie = Movie(title=title, description=description, image=image,category=category, year=year,actors=actors,release_date=release_date, url=url)
            movie.save()
            next_url = request.POST.get('next', reverse('home'))
            return redirect(next_url)

        else:
            # Handle the case where required fields are missing
            return render(request, 'add.html', {'error': 'All fields except URL are required'})

    else:
        return render(request, 'add.html')

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        next_url = request.POST.get('next', reverse('home'))
        return redirect(next_url)
    return render(request, 'confirm_delete.html', {'movie': movie})

def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie:detail', movie_id=movie.id)
    else:
            form = MovieForm(instance=movie)
    return render(request, 'update_movie.html', {'form': form, 'movie': movie})