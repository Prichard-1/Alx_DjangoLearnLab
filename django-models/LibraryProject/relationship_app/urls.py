from django.urls import path
from . import views

urlpatterns = [
    # 🔐 Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # 📘 Book Management with Permissions
    path('books/', views.list_books, name='list_books'),
    path('add_book/', views.add_book, name='add_book'),  # ✅ Updated for checker
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),  # ✅ Updated for checker
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    # 🧑‍💼 Role-Based Views
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
]
