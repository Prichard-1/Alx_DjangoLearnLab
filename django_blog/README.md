# 📝 Django Blog Project

A full-featured blogging platform built with Django. This project includes user authentication, post management, commenting, and profile customization — designed to meet real-world development standards and ALX evaluation criteria.

---

## 🚀 Features

### 🔐 Authentication
- User registration, login, and logout
- Profile view and edit (username, email)
- Optional extension: bio and profile picture via `UserProfile` model

### 📝 Blog Posts
- Create, read, update, delete (CRUD) operations
- Posts linked to authenticated authors
- Published date auto-generated

### 💬 Comments
- Users can comment on posts
- Authenticated users can edit/delete their own comments
- Comments displayed under each post

### 🏷️ Tags & 🔎 Search
- Posts can be tagged for categorization
- Search functionality for title, content, and tags

---

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/your-username/Alx_DjangoLearnLab.git
cd django_blog

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver
