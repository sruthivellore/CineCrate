from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Rented
from django.utils import timezone
from django.conf import settings
from .models import Customer
import json
import re


def load_movies():
    json_file_path = settings.BASE_DIR / 'static' / 'movies.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
def load_movie_images():
    json_file_path = settings.BASE_DIR / 'static' / 'movie_images.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
def load_cast_images():
    json_file_path = settings.BASE_DIR / 'static' / 'movie_cast_images.json'
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def movie_detail(request, id):
    rented_info = get_rented_movies_info(request.user) if request.user.is_authenticated else {
        'all_rented_movies': set(),
        'user_rented_movies': set()
    }
    all_movies = load_movies()
    movies_images = load_movie_images()
    cast_images = load_cast_images()
    movie = next((movie for movie in all_movies if movie['id'] == id), None) 
    movie_images = movies_images[str(id)] 
    movie_cast_images = cast_images[str(id)]
    print(movie, rented_info)
    return render(request, 'store/movie_detail.html', {'rented_info' : rented_info,'movie': movie, 'movie_images': movie_images,'movie_cast_images': movie_cast_images})

def apply_filters(movies, search, genre, year, rating):
    if search:
        movies = [m for m in movies if search in m['title'].lower()]
    if genre:
        movies = [m for m in movies if genre.lower() in [g.lower() for g in m['genre']]]
    if year:
        movies = [m for m in movies if str(m['releaseYear']) == year]
    if rating:
        try:
            r = float(rating)
            movies = [m for m in movies if float(m.get('rating', 0)) >= r]
        except ValueError:
            pass
    return movies

def apply_sorting(movies, sort_by):
    if sort_by == 'rating':
        return sorted(movies, key=lambda m: float(m.get('rating', 0)), reverse=True)
    elif sort_by == 'year':
        return sorted(movies, key=lambda m: int(m.get('releaseYear', 0)), reverse=True)
    elif sort_by == 'title':
        return sorted(movies, key=lambda m: m.get('title', '').strip().lower()[:1])
    return movies  

def paginate_items(items, page_number, per_page=12):
    paginator = Paginator(items, per_page)
    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1

    if page_number > paginator.num_pages:
        page_number = paginator.num_pages

    return paginator.get_page(page_number)

def store(request):
    all_movies = load_movies()
    search = request.GET.get('search', '').lower()
    genre = request.GET.get('genre')
    year = request.GET.get('year')
    rating = request.GET.get('rating')
    sort_by = request.GET.get('sort_by')
    page_number = request.GET.get('page')

    filtered = apply_filters(all_movies, search, genre, year, rating)
    sorted_movies = apply_sorting(filtered, sort_by)
    page_obj = paginate_items(sorted_movies, page_number)

    top_movies = [m for m in filtered if float(m.get('rating', 0)) >= 8.0]
    top_movies = apply_sorting(top_movies, 'rating')
    top_movies = apply_sorting(top_movies, sort_by)
    top_movies = paginate_items(top_movies, page_number)

    latest_movies = [m for m in filtered if float(m.get('releaseYear', 0)) >= 2020]
    latest_movies = apply_sorting(latest_movies, sort_by)
    latest_movies = apply_sorting(latest_movies, 'releaseYear')
    latest_movies = paginate_items(latest_movies, page_number)

    genres = sorted(set(g for m in all_movies for g in m['genre']))
    years = sorted(set(str(m['releaseYear']) for m in all_movies), reverse=True)

    querystring = '&'.join([f"{k}={v}" for k, v in request.GET.items() if k != 'page'])

    rented_info = get_rented_movies_info(request.user) if request.user.is_authenticated else {
        'all_rented_movies': set(),
        'user_rented_movies': set()
    }
    user_rented_movies = []
    if request.user.is_authenticated:
        user_rented_ids = rented_info['user_rented_movies']
        user_rented_movies = [m for m in all_movies if int(m['id']) in user_rented_ids]
    user_rented_movies = apply_filters(user_rented_movies, search, genre, year, rating)
    user_rented_movies = apply_sorting(user_rented_movies, sort_by)
    user_rented_movies = paginate_items(user_rented_movies, page_number)

    return render(request, 'store/Store.html', {
        'page_obj': page_obj,
        'genres': genres,
        'years': years,
        'top_movies': top_movies,
        'latest_movies': latest_movies,
        'request': request,
        'querystring': querystring,
        'rented_info':rented_info,
        'user_rented_movies': user_rented_movies

    })

@login_required
def custom_logout(request):
    logout(request)
    return redirect('custom_login') 

def is_strong_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    )


@csrf_protect
def custom_login(request):
    all_movies = load_movies()
    latest_movies = sorted(all_movies, key=lambda x: x['releaseYear'], reverse=True)[:10]
    image_urls = [movie['image'] for movie in latest_movies]

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome back.')
            return redirect('store')
        else:
            return render(request, 'user_auth/login.html', {
                'error': 'Invalid credentials',
                'image_urls': image_urls
            })

    return render(request, 'user_auth/login.html', {'image_urls': image_urls})


@csrf_protect
def signup(request):
    all_movies = load_movies()
    image_urls = [movie['image'] for movie in all_movies][:10]

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        if password != confirm_password:
            return render(request, 'user_auth/signup.html', {
                'error': "Passwords do not match.",
                'image_urls': image_urls
            })

        if not is_strong_password(password):
            return render(request, 'user_auth/signup.html', {
                'error': "Password: 8+ characters, uppercase, lowercase, number and special character.",
                'image_urls': image_urls
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'user_auth/signup.html', {
                'error': "Username already taken.",
                'image_urls': image_urls
            })
        if User.objects.filter(email=email).exists():
            return render(request, 'user_auth/signup.html', {
                'error': "Email already taken.",
                'image_urls': image_urls
            })

        user = User.objects.create_user(username=username, email=email, password=password)
        Customer.objects.create(user=user, email=email)
        messages.success(request, f"Welcome {username}, your account has been created!")
        return render(request, 'user_auth/login.html', {
                'success': 'Your account has been created! Kindly Login.',
                'image_urls': image_urls
            })

    return render(request, 'user_auth/signup.html', {'image_urls': image_urls})


@login_required
@require_POST
def rent_movie(request, movie_id):
    user = request.user

    # Example fixed rental charge — adjust as needed
    rental_charge = 4.99

    rented_movie = Rented.objects.create(
        movie_id=movie_id,
        user=user,
        charges=rental_charge,
        start_date=timezone.now()
    )
    rented_movie.save()
    messages.success(request, "Movie rented successfully!")
    return redirect('movie_detail', id=movie_id)

def get_rented_movies_info(user: User):

    all_rented_ids = set(int(mid) for mid in Rented.objects.values_list('movie_id', flat=True))
    user_rented_ids = set(int(mid) for mid in Rented.objects.filter(user=user).values_list('movie_id', flat=True))

    return {
        'all_rented_movies': all_rented_ids,
        'user_rented_movies': user_rented_ids,
    }

@login_required
@require_POST
def return_movie(request, movie_id):
    Rented.objects.filter(user=request.user, movie_id=movie_id).delete()
    messages.success(request, "Movie returned successfully!")
    return redirect('movie_detail', id=movie_id)
