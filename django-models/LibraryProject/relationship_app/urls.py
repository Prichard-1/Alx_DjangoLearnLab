from django.urls import path
from .views import (
    login_view,
    logout_view,
    register_view,
    list_books,
    admin_view,
    librarian_view,
    member_view
)

urlpatterns = [
    # 🔐 Authentication URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # 📚 Book Listing
    path('books/', list_books, name='list_books'),

    # 🛡️ Role-Based Access Control
    path('admin/', admin_view, name='admin_view'),
    path('librarian/', librarian_view, name='librarian_view'),
    path('member/', member_view, name='member_view'),
]

