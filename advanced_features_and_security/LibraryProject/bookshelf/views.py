from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # your view logic

