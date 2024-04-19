from django.contrib import admin
from .models import Book,Borrow,Category,Review
# Register your models here.
admin.site.register(Book)
admin.site.register(Borrow)
admin.site.register(Category)
admin.site.register(Review)