from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author = Author.objects.get(name="Chinua Achebe")
print("Books by Chinua Achebe:")
for book in Book.objects.filter(author=author):
    print(f"- {book.title}")

# List all books in a library
library = Library.objects.get(name="Central Library")
print("\nBooks in Central Library:")
for book in library.books.all():
    print(f"- {book.title} by {book.author.name}")

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print(f"\nLibrarian for Central Library: {librarian.name}")

