from rest_framework import serializers
from .models import Author, Book
import datetime

# BookSerializer: Serializes all fields of the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation to ensure publication_year is not in the future
    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

# AuthorSerializer: Includes name and nested books
class AuthorSerializer(serializers.ModelSerializer):
    # Nested BookSerializer to show all books by the author
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
i
