from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings
import json

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
    all_movies = load_movies()
    movies_images = load_movie_images()
    cast_images = load_cast_images()
    movie = next((movie for movie in all_movies if movie['id'] == id), None) 
    movie_images = movies_images[str(id)] 
    movie_cast_images = cast_images[str(id)]
    return render(request, 'store/movie_detail.html', {'movie': movie, 'movie_images': movie_images,'movie_cast_images': movie_cast_images})

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

    return render(request, 'store/Store.html', {
        'page_obj': page_obj,
        'genres': genres,
        'years': years,
        'top_movies': top_movies,
        'latest_movies': latest_movies,
        'request': request,
        'querystring': querystring,
    })
