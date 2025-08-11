from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from .models import Book, UserProfile
from .forms import BookForm


# ==============================
# 🔹 Helper Role Check Functions
# ==============================
def is_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# ==============================
# 🔹 Authentication Views
# ==============================
def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})


def logout_view(request):
    """Logs out the current user."""
    logout(request)
    return render(request, 'relationship_app/logout.html')


def register_view(request):
    """Handles new user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# ==============================
# 🔹 Book Listing
# ==============================
@login_required
def list_books(request):
    """Displays a list of all books."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# ==============================
# 🔹 Role-Based Access Views
# ==============================
@login_required
@user_passes_test(is_admin, login_url='/login/', raise_exception=True)
def admin_view(request):
    """Admin-only dashboard view."""
    return render(request, 'relationship_app/admin_view.html')


@login_required
@user_passes_test(is_librarian, login_url='/login/', raise_exception=True)
def librarian_view(request):
    """Librarian-only view."""
    return render(request, 'relationship_app/librarian_view.html')


@login_required
@user_passes_test(is_member, login_url='/login/', raise_exception=True)
def member_view(request):
    """Member-only view."""
    return render(request, 'relationship_app/member_view.html')


# ==============================
# 🔹 Permission-Protected Book Actions
# ==============================
@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """Add a new book (requires can_add_book permission)."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})


@login_required
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """Edit an existing book (requires can_change_book permission)."""
    book = get_object_or_404(Book, id=book_id)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('list_books')
    return render(request, 'relationship_app/edit_book.html', {'form': form})


@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """Delete a book (requires can_delete_book permission)."""
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

