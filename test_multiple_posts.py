import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mb_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

# Clean up test data if exists
User.objects.filter(username='multipost_test').delete()

# Create test user
user = User.objects.create_user('multipost_test', password='test123')
print(f"✓ Created user: {user.username}")

# Create multiple posts for the same user
posts_data = [
    "This is my first post!",
    "Here's another post from the same user.",
    "And yet another one - proving multiple posts work!",
    "Fourth post - no limits here!",
    "Fifth post - users can post as many times as they want!"
]

for i, text in enumerate(posts_data, 1):
    Post.objects.create(text=text, author=user)
    print(f"✓ Created post {i}: {text[:40]}...")

# Verify
user_posts = Post.objects.filter(author=user)
print(f"\n✅ SUCCESS: User '{user.username}' now has {user_posts.count()} posts!")
print("\nAll posts:")
for post in user_posts:
    print(f"  - {post.text[:50]}")

# Clean up
print(f"\n🧹 Cleaning up test data...")
user.delete()
print("✓ Test user and posts deleted")
