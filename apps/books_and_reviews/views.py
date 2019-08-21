from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request):
    if 'curUser' not in request.session:
        return redirect('/')
    reviews = Reviews.objects.all()
    reversedReviews = reviews[::-1]
    finalReviews = reversedReviews[:3]
    for review in finalReviews:
        #htmlString = ""
        stars = []
        for i in range(review.rating):
            stars.append(1)
            #htmlString += "<img src= \"{% static '/books_and_reviews/images/gold_star.png' %}\" alt='Gold Star' height='40'>"
        for i in range(5 - review.rating):
            stars.append(0)
            #htmlString += "<img src= \"{% static '/books_and_reviews/images/outline_star.png' %}\" alt='Empty Star' height='40'>"
        #review.rating = htmlString
        review.rating = stars
    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'books' : Books.objects.all(),
        'reviews' : finalReviews
    }
    return render(request, 'books_and_reviews/index.html', context)

def add_book(request):
    if 'curUser' not in request.session:
        return redirect('/')
    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'authors' : Authors.objects.all()
    }
    print(context['authors'])
    return render(request, 'books_and_reviews/add.html', context)

def show_book(request, book_id):
    if 'curUser' not in request.session:
        return redirect('/')
    book = Books.objects.get(id = book_id)
    reviews = book.reviews.all()
    for review in reviews:
        #htmlString = ""
        stars = []
        for i in range(review.rating):
            stars.append(1)
            #htmlString += "<img src= \"{% static '/books_and_reviews/images/gold_star.png' %}\" alt='Gold Star' height='40'>"
        for i in range(5 - review.rating):
            stars.append(0)
            #htmlString += "<img src= \"{% static '/books_and_reviews/images/outline_star.png' %}\" alt='Empty Star' height='40'>"
        #review.rating = htmlString
        review.rating = stars
    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'book' : book,
        'reviews' : reviews
    }
    return render(request, 'books_and_reviews/book_details.html', context)

def delete_review(request, review_id):
    review = Reviews.objects.get(id = review_id)
    book_id = review.book.id
    review.delete()
    return redirect('/books/' + str(book_id))

def add_book_and_review(request):
    if 'title' not in request.POST:
        book = Books.objects.get(id = request.POST['book_id'])
    else:
        errors = Books.objects.book_validator(request.POST)
        if Books.objects.filter(title=request.POST['title']).exists():
            errors['exists'] = "A book with this title already exists!"
        if ('selected_author' not in request.POST) and (len(request.POST['new_author']) == 0):
            errors['author'] = "The book must have an author!"
        if Authors.objects.filter(name=request.POST['new_author']).exists():
            errors['exists'] = "An author with this name already exists!"
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books/add')
        if len(request.POST['new_author']) > 0:
            Authors.objects.create(name = request.POST['new_author'])
            author = Authors.objects.get(name = request.POST['new_author'])
        else:
            author = Authors.objects.get(id = request.POST['selected_author'])
        Books.objects.create(title = request.POST['title'], uploaded_by = Users.objects.get(id = request.session['curUser']),
                        written_by = author)
        book = Books.objects.get(title = request.POST['title'])
    Reviews.objects.create(content = request.POST['review'], rating = int(request.POST['rating']), 
            book = book, created_by = Users.objects.get(id = request.session['curUser']))
    return redirect('/books/' + str(book.id))
