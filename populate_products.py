import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')
django.setup()

from store.models import Product

sample = [
    {'title':'Red T-Shirt','description':'Comfortable cotton T-shirt','price':'19.99','stock':50,'slug':'red-tshirt'},
    {'title':'Blue Jeans','description':'Classic denim jeans','price':'49.99','stock':20,'slug':'blue-jeans'},
    {'title':'Sneakers','description':'Running shoes','price':'69.99','stock':15,'slug':'sneakers'},
]

for s in sample:
    p, created = Product.objects.get_or_create(slug=s['slug'], defaults={
        'title':s['title'],'description':s['description'],'price':s['price'],'stock':s['stock']
    })
    print(('Created' if created else 'Exists') + ':', p.title)

print('Done')
