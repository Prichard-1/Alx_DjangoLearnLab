from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# ==========================
# 🔹 Custom User Manager
# ==========================
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

# ==========================
# 🔹 Custom User Model
# ==========================
class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

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
    Extends the CustomUser model with role-based access control.
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    class Meta:
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# 🛎️ Signal to auto-create UserProfile on CustomUser creation
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a UserProfile for every newly created CustomUser.
    Defaults to 'Member' role.
    """
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance, role='Member')
