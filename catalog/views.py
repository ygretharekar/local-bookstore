from django.shortcuts import render

# Create your views here.

from .models import Book, BookInstance, Author, Genre




def index(request):
	'''
	View function for home page site
	'''
	num_books = Book.objects.all().count()  # pylint: disable=E1101
	num_instances = BookInstance.objects.all().count()  # pylint: disable=E1101
	num_instances_available = BookInstance.objects.filter(  # pylint: disable=E1101
		status__exact='a').count()

	num_authors = Author.objects.count()  # pylint: disable=E1101

	return render(
		request,
		'index.html',
		context={
			'num_books':num_books,
			'num_instances':num_instances,
			'num_instances_available':num_instances_available,
			'num_authors':num_authors,
		}
	)

from django.views import generic

class BookListView(generic.ListView):
	model = Book




