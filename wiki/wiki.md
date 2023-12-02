Here are some of the scripts I have used trough out this project.

1. Generate lots of dummy users.

```python
import os
import django
import requests
from django.core.files.base import ContentFile

from UserProfile.models import BargadUser
from faker import Faker
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bargad.settings')
django.setup()

# Create an instance of the Faker class
fake = Faker()


def fetch_and_save_image():
    image_url = 'https://i.pravatar.cc/200'
    response = requests.get(image_url)
    if response.status_code == 200:
        return ContentFile(response.content)
    return None


# Create 100 dummy users
for _ in range(1000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = fake.user_name()
    email = fake.email()
    password = fake.password()

    # Create a new User object and save it
    user = BargadUser.objects.create_user(username=username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name

    # Create a dummy profile picture for the user
    image_content = fetch_and_save_image()
    if image_content:
        user.profile_picture.save('post_image.jpg', image_content, save=True)

    user.user_type = random.randint(1, 7)
    user.save()

print("1000 dummy users with first names, last names, and profile pictures created successfully.")
```

2. Generate lots of dummy posts.

```python

import random
import uuid
import requests
from django.core.files.base import ContentFile
from faker import Faker
from django.contrib.auth import get_user_model
from Post.models import Post  # Replace 'myapp' with your actual app name

fake = Faker()
User = get_user_model()


# Function to fetch and save an image
def fetch_and_save_image():
    image_url = 'https://source.unsplash.com/user/c_v_r'
    response = requests.get(image_url)
    if response.status_code == 200:
        return ContentFile(response.content)
    return None


# Create 1000 dummy posts
for _ in range(1000):
    # Get a random user
    random_user = User.objects.order_by('?').first()

    # Create a dummy post
    post = Post.objects.create(
        user=random_user,
        caption=fake.text(max_nb_chars=120),
        description=fake.text(max_nb_chars=520),
    )

    # Fetch and save the image
    image_content = fetch_and_save_image()
    if image_content:
        post.image.save('post_image.jpg', image_content, save=True)

    # Randomly set shared_from and original_post
    if random.random() < 0.3:  # 30% chance of being shared
        shared_from = Post.objects.order_by('?').first()
        post.shared_from = shared_from
        shared_from.share_count += 1
        shared_from.save()
    if random.random() < 0.2:  # 20% chance of being edited
        original_post = Post.objects.order_by('?').first()
        post.original_post = original_post
        original_post.edit_count += 1
        original_post.save()

    post.save()

```

3. Generate lots of dummy students, teachers, and staffs.

```python
import os
import random

import django
from faker import Faker

from UserProfile.models import BargadUser
from UserProfile.models import StudentUserProfile, StaffUserProfile, TeacherUserProfile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bargad.settings')
django.setup()

# Create an instance of the Faker class
fake = Faker()

# creating lots of dummy students for testing

students = BargadUser.objects.filter(user_type=BargadUser.UT_STUDENT)

for student in students:
    obj = StudentUserProfile.objects.create(user=student)

    obj.father_name = fake.short_name()
    obj.mother_name = fake.short_name()
    obj.guardian_name = fake.short_name()

    obj.dob = fake.date()
    obj.gender = random.randint(1, 3)
    obj.c_address = fake.address()
    obj.p_address = fake.address()

    obj.primary_contact = fake.phone_number()
    obj.secondary_contact = fake.phone_number()

    obj.bio = fake.text()

    obj.is_alumni = random.choice([True, False])
    obj.parent_contact = fake.phone_number()

    obj.save()

print("1000 dummy students created successfully.")

teachers = BargadUser.objects.filter(user_type=BargadUser.UT_TEACHER)

for teacher in teachers:
    obj = TeacherUserProfile.objects.create(user=teacher)

    obj.dob = fake.date()
    obj.gender = random.randint(1, 3)
    obj.c_address = fake.address()
    obj.p_address = fake.address()

    obj.primary_contact = fake.phone_number()
    obj.secondary_contact = fake.phone_number()
    obj.bio = fake.text()

    obj.qualification = fake.text()
    obj.experience = fake.text()
    obj.designation = fake.text()

    obj.save()

print("1000 dummy teachers created successfully.")

staffs = BargadUser.objects.filter(user_type=BargadUser.UT_STAFF)

for staff in staffs:
    obj = StaffUserProfile.objects.create(user=staff)

    obj.dob = fake.date()
    obj.gender = random.randint(1, 3)
    obj.c_address = fake.address()
    obj.p_address = fake.address()

    obj.primary_contact = fake.phone_number()
    obj.secondary_contact = fake.phone_number()

    obj.bio = fake.text()

    obj.post = fake.text()

    obj.save()

print("1000 dummy staffs created successfully.")
```