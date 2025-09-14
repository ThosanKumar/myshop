import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@example.com'
password = 'AdminPass123!'

u = User.objects.filter(username=username).first()
if u is None:
    User.objects.create_superuser(username, email, password)
    print('SUPERUSER_CREATED')
else:
    u.set_password(password)
    u.email = email
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('SUPERUSER_UPDATED')

print(f'credentials: username={username} password={password}')
