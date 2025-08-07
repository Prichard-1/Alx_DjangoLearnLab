

##Create
python manage.py shell
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949):

##Retrieve
python manage.py shell
retrieved_book = Book.objects.get(title="1984")

##Update
python manage.py shell
book.title = "Nineteen Eighty-Four"
book.save()


##Delete
 python manage.py shell
  book.delete()
  Book.objects.all()  # should return an empty queryset
