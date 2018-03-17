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

	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1



	return render(
		request,
		'index.html',
		context={
			'num_books':num_books,
			'num_instances':num_instances,
			'num_instances_available':num_instances_available,
			'num_authors':num_authors,
			'num_visits': num_visits
		}
	)

from django.views import generic

class BookListView(generic.ListView):
	model = Book
	paginate_by = 2

	def get_context_data(self, **kwargs):
		context = super(BookListView, self).get_context_data(**kwargs)

		context['name'] = 'ygr'

		return context



class BookDetailView(generic.DetailView):
	model = Book


class AuthorListView(generic.ListView):
	model = Author


class AuthorDetailView(generic.DetailView):
	model = Author


from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	"""
    Generic class-based view listing books on loan to current user. 
    """
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(  # pylint: disable=E1101
				borrower = self.request.user
			).filter(
				status__exact = 'o'
			).order_by(
				'due_back'
			)

from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
	"""
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """

	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name = 'catalog/bookinstance_list_borrowed_all.html'
	paginate_by = 10

	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')  # pylint: disable=E1101


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

from .forms import RenewBookForm


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
	"""
    View function for renewing a specific BookInstance by librarian
    """
	book_inst=get_object_or_404(BookInstance, pk = pk)

	if request.method == 'POST':

		form = RenewBookForm(request.POST)

		if form.is_valid():
			book_inst.due_back = form.cleaned_data['renewal_date']
			book_inst.save()

			return HttpResponseRedirect(reverse('all-borrowed') )

	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

	return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'



class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


from django.http import JsonResponse

def JSONResponseClass(request):
	return JsonResponse({'Hello': request.GET})



