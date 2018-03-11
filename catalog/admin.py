from django.contrib import admin

# Register your models here.

from .models import Author, Book, BookInstance, Language, Genre

# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Language)
admin.site.register(Genre)



class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth')
	fields = ['first_name', 'last_name','date_of_birth']

admin.site.register(Author, AuthorAdmin)


class BookInstanceInline(admin.TabularInline):
	model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre', 'display_lang')
	inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('display_title', 'display_loan_status', 'due_back')
	list_filter=('status', 'due_back')

	fieldsets = (
		(
			None,
			{
				'fields': (
					'book',
					'imprint',
					'id'
				)
			}
		),
		(
			'Availability',
			{
				'fields': (
					'status',
					'due_back'
				)
			}
		)
	)



