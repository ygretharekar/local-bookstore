from django.db import models

# Create your models here.

class Genre(models.Model):
	'For book Genre'
	name = models.CharField(max_length = 200, help_text = 'Enter book Genre')
	def __str__(self):
		
		return self.name


from django.urls import reverse

class Book(models.Model):
	'Model representing book'

	title = models.CharField(max_length=200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	summary = models.TextField(max_length=1000, help_text='Enter brief description of book')
	isbn = models.CharField('ISBN', max_length=13, help_text='13 chars')
	genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
	language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		'''
		String to represent the model object
		'''
		return self.title


	def get_absolute_url(self):
		'''
		Return the url to access detail record for this book
		'''
		return reverse('book-detail', args=[str(self.id)])  # pylint: disable=E1101


import uuid

class BookInstance(models.Model):
	'''
	Model Representing specific copy of book
	'''

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique id for book')
	book = models.ForeignKey('Book', on_delete = models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)

	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved')
	)

	status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

	class Meta:
		ordering = ['due_back']

	def __str__(self):
		'''
		String for representing model object
		'''
		return f'{self.id} ({self.book.title})'  # pylint: disable=E1101



class Author(models.Model):
	'''
	Model Representing author
	'''
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		 '''
		 Returns url to access perticular author instance
		 '''

		 return reverse('author-detail', args=[str(self.id)]) # pylint: disable=E1101

	def __str__(self):
		'''
		String representing the object
		'''

		return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
	'''
	Gives language of books
	'''

	name = models.CharField(max_length=100, help_text='Language of the book')

	def __str__(self):
		'''
		Returns name in string form
		'''

		return self.name
