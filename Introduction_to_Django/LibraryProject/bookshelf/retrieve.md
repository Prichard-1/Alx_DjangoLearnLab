# Retrieve Book Instance from Django Shell

```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book
# <Book: 1984>


