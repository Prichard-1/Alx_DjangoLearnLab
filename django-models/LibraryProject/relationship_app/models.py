from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 📚 Author Model
class Author(models.Model):
    """
    Represents an author of books.
    """
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


# 📘 Book Model with Custom Permissions
class Book(models.Model):
    """
    Represents a book in the library.
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title


# 🏛️ Library Model
class Library(models.Model):
    """
    Represents a library containing multiple books.
    """
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, blank=True)

    class Meta:
        verbose_name_plural = "Libraries"

    def __str__(self):
        return self.name


# 👩‍💼 Librarian Model
class Librarian(models.Model):
    """
    Represents a librarian responsible for a specific library.
    """
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Librarians"

    def __str__(self):
        return self.name


# 🔐 UserProfile Model for Role-Based Access
class UserProfile(models.Model):
    """
    Extends the User model with role-based access control.
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# 🛎️ Signal to auto-create UserProfile on User creation
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a UserProfile for every newly created User.
    Defaults to 'Member' role.
    """
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance, role='Member')
