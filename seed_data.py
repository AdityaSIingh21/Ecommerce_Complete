from decimal import Decimal
from django.contrib.auth.models import User
from shop.models import Category, Product
def img_path(name): return f'products/{name}'
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin','admin@example.com','admin123'); print('Created admin user')
cats = ['Electronics','Fashion','Home & Kitchen']; cat_objs={}
for c in cats: obj,_=Category.objects.get_or_create(name=c); cat_objs[c]=obj
products=[
    ('iPhone 14','Electronics','79999.00','iphone.jpg','Latest Apple iPhone.'),
    ('MacBook Air M2','Electronics','114900.00','macbook.jpg','Slim laptop.'),
    ('Sony Headphones','Electronics','7999.00','headphones.jpg','Noise cancelling.'),
    ('T-Shirt Classic','Fashion','799.00','tshirt.jpg','Comfortable cotton tee.'),
    ('Slim Fit Jeans','Fashion','1499.00','jeans.jpg','Stretch denim.'),
    ('Sneakers Nike','Fashion','3499.00','sneakers.jpg','Casual sneakers.'),
    ('Coffee Maker Pro','Home & Kitchen','2499.00','coffee_maker.jpg','Brew rich coffee.'),
    ('Blender 500W','Home & Kitchen','1999.00','blender.jpg','Powerful blender.'),
    ('Sofa 3-Seater','Home & Kitchen','25999.00','sofa.jpg','Comfortable fabric sofa.'),
    ('Dining Set 6pcs','Home & Kitchen','18499.00','dining_set.jpg','Modern dining set.'),
]
for name,cat,price,img,desc in products:
    Product.objects.get_or_create(name=name,defaults={'description':desc,'price':Decimal(price),'image':img_path(img),'category':cat_objs[cat]})
print('Seed complete')
