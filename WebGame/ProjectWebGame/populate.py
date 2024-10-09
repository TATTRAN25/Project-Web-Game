import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from ProjectWebGame.models import UserProfileInfo, Developer, Category, Game, Review

# Thiết lập Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebGame.settings')
django.setup()

# Khởi tạo Faker
fake = Faker()

def create_users(n=10):
    users = []
    for _ in range(n):
        username = fake.user_name()
        email = fake.email()
        user = User.objects.create_user(username=username, email=email, password='password')
        UserProfileInfo.objects.create(user=user, address=fake.address(), bio=fake.text())
        users.append(user)
    return users

def create_developers(n=5):
    for _ in range(n):
        Developer.objects.create(
            name=fake.company(),
            description=fake.text(),
            website=fake.url(),
            logo=''  # Để trống trường logo
        )

def create_categories(n=3):
    for _ in range(n):
        Category.objects.create(
            name=fake.word(),
            description=fake.text()
        )

def create_games(n=20):
    developers = Developer.objects.all()
    categories = Category.objects.all()
    
    for _ in range(n):
        Game.objects.create(
            name=fake.catch_phrase(),
            developer=random.choice(developers),
            category=random.choice(categories),
            description=fake.text(),
            image='',  # Để trống trường hình ảnh
            link_dowload=fake.url(),
            release_date=fake.date_this_decade(),
            is_published=random.choice([True, False])
        )

def create_reviews(n=50):
    users = User.objects.all()
    games = Game.objects.all()
    
    for _ in range(n):
        Review.objects.create(
            user=random.choice(users),
            game=random.choice(games),
            content=fake.text(),
            rating=random.uniform(0, 10),
            is_published=random.choice([True, False])
        )

if __name__ == '__main__':
    create_users()
    create_developers()
    create_categories()
    create_games()
    create_reviews()
    print("Dữ liệu mẫu đã được tạo thành công!")