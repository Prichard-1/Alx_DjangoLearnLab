from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Shows these columns in admin list view
    list_filter = ('author', 'publication_year')           # Adds filter sidebar by author and year
    search_fields = ('title', 'author')                    # Enables search by title and author
