# 🎬 CineCrate

CineCrate is a responsive, user-friendly Django web application designed for movie browsing and rental. It offers features like advanced search, filtering, sorting, poster previews, and a simple rental system — all wrapped in a clean, Bootstrap-styled layout.

---

## ✨ Features

* **Movie Catalog**: Browse through a curated list of movies loaded from a JSON file.
* **Search and Filter**: Quickly find movies by title, genre, or release year.
* **Sort Options**: Sort movies by rating, release date, and more.
* **Hover Previews**: View movie posters instantly by hovering over titles.
* **Top Rated and Latest Tabs**: Explore top-rated and newly added movies.
* **Rental System**: Rent available movies; availability status updates dynamically.
* **Responsive Design**: Built with Bootstrap for mobile-first responsiveness.
* **Custom Theme**: Soft animations, consistent color palette, and neatly styled movie cards.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Django 4.x
* pip (Python package manager)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sruthivellore/CineCrate.git
   cd CineCrate
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/Scripts/activate 
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Open your browser and visit:

   ```
   http://127.0.0.1:8000/
   ```
## 🧭 Navigating the App

### **Browsing Movies**

You can view all available movies and their details **without logging in**. Simply visit the homepage, and you'll be able to:

* Browse through the list of movies.
* Search movies by title, genre, or year.
* Sort movies by release date or rating.
* View hover previews of movie posters and click on it for more details.

### **Renting Movies (Login Required)**

To rent movies, you must first **sign up** or **log in** to the app. Here's how:

1. **Sign Up**:
   Click on the "Sign Up" link in the top navigation bar. You'll need to provide a username, email, and password to create an account.

2. **Login**:
   If you already have an account, click on the "Login" link, enter your credentials, and you'll be able to access the movie rental system.

3. **Renting Movies**:
   Once logged in, simply click on the "Rent" button next to any available movie to rent it. The rental status will be updated accordingly.

---

## 📁 Project Structure

Here’s a breakdown of the project structure:

### **CineCrate/**: Main app directory

Contains the core files and settings for the Django project.

* **`__init__.py`**: Marks the directory as a Python package.
* **`asgi.py`**: ASGI configuration for asynchronous support.
* **`settings.py`**: Settings for the Django project (database, apps, middleware, etc.).
* **`urls.py`**: URL routing for the entire project.
* **`wsgi.py`**: WSGI configuration for deployment.

### **static/**: Static files (assets used for styling, scripts, etc.)

Contains all the static files for the project.

* **`css/`**: CSS styles for the project.
* **`images/`**: Image assets like movie posters or icons.
* **`js/`**: JavaScript files for functionality.
* **movie\_cast\_images.json, movie\_images.json, movies.json**: Movie data in JSON format


### **store/**: Django app for movie storage and logic

Handles the logic for storing and managing movie data, as well as the rental functionality.

* **`__init__.py`**: Marks the directory as a Python package.
* **`admin.py`**: Configuration for Django admin interface.
* **`apps.py`**: Configuration for the Django app.
* **`models.py`**: Defines the app’s models (e.g., Movie, Rental).
* **`tests.py`**: Contains tests for the app.
* **`urls.py`**: URL routing specific to the store app.
* **`views.py`**: Defines views to handle the business logic.
* **migrations/**: Database migration files
* **templates/**: HTML templates

### **db.sqlite3**: SQLite database file

This is the default database file that stores all the data for your project (e.g., users, movie rentals).

### **manage.py**: Django management script

The script used to run server commands, make migrations, migrate the database, and more.

## 🛠️ Built With

* [Django](https://www.djangoproject.com/) - Web framework
* [Bootstrap](https://getbootstrap.com/) - Front-end styling
* HTML5, CSS3, JavaScript

