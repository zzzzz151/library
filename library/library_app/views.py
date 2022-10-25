from django.shortcuts import render, redirect
from datetime import datetime
from library_app.models import *


# Create your views here.

def home(request):
    tparams = {
        'title': 'Home of Library app',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)

def allBooks(request):
    books = Book.objects.all()
    tparams = {
        'books' : books
    }
    return render(request, 'allBooks.html', tparams)

def bookDisplay(request, bookId):
    tparams = {
        'book' : Book.objects.get(id=bookId)
    }
    return render(request, 'bookDisplay.html', tparams)

def bookSearch(request):
    if 'queryBookTitle' in request.POST:
        query = request.POST['queryBookTitle']
        if query:
            books = Book.objects.filter(title__icontains=query)
            return render(request, 'bookList.html', {'boks':books, 'query':query})
        else:
            return render(request, 'bookSearch.html', {'error':True})
    elif 'queryBookAuthorOrPublisher' in request.POST:
        query = request.POST['queryBookAuthorOrPublisher']
        if query:
            books = Book.objects.filter(publisher__name__icontains=query)
            books = books.union(Book.objects.filter(authors__name__icontains=query))
            return render(request, 'bookList.html', {'boks': books, 'query': query})
        else:
            return render(request, 'bookSearch.html', {'error': True})
    elif 'queryAuthor' in request.POST:
        query = request.POST['queryAuthor']
        if query:
            authors = Author.objects.filter(name__icontains=query)
            return render(request, 'authorList.html', {'authors': authors, 'query': query})
        else:
            return render(request, 'authorList.html', {'error': True})
    else:
        # first time acessing
        return render(request, 'bookSearch.html', {'error':False})

def insert(request):
    # TODO: implement add publisher and add author

    #  if not request.user.is_authenticated or request.user.username != "admin":
    if not request.user.is_authenticated:
        return redirect("/login")

    if "bookTitle" in request.POST:
        valid = True
        if request.POST["bookTitle"] == "":
            valid = False
        if valid:
            # User added a book
            bookTitle = request.POST["bookTitle"]
            publisherNameSelected = request.POST["publisherSelected"]
            publisherSelected = Publisher.objects.get(name=publisherNameSelected)
            newBook = Book(title=bookTitle,
                           publisher=publisherSelected,
                           date=datetime.now())
            newBook.save()
            authorsNamesSelected = request.POST.getlist("authorsSelected")
            authorsSelected = []
            allAuthors = Author.objects.all()
            for authorName in authorsNamesSelected:
                au = Author.objects.get(name=authorName)
                authorsSelected.append(au)
            newBook.authors.set(authorsSelected)

    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    data = {}
    data["authors"] = authors
    data["publishers"] = publishers
    return render(request, "insert.html", data)

def edit(request):
    # TODO: allow edit publisher and book
    #for key in request.POST:
        #print("<" + key + ", " + request.POST[key] +">")
    authors = Author.objects.all()
    for author in authors:
        varAuthorName = str(author.id) + author.name
        if varAuthorName not in request.POST:
            continue
        #print("updating " + author.name)
        varAuthorEmail = str(author.id) + str(author.email)
        author.name = request.POST[varAuthorName]
        author.email = request.POST[varAuthorEmail]
        author.save()

    data = {}
    authors = Author.objects.all() # refresh just in case
    data["authors"] = authors
    return render(request,"edit.html",data)

from library_app.forms import *

# Using Django Form
def bookQuery(request):
    if request.method == "POST":
        # pass data to BookQueryForm object
        form = BookQueryForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["query"]
            books = Book.objects.filter(title__icontains=query)
            data = {"boks": books, "query": query}
            return render(request, "bookList.html", data)
    else: # if GET or other method
        form = BookQueryForm()
    return render(request, "bookQuery.html", {"form" : form})
