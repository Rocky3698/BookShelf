from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.ManyToManyField(Category,related_name='boot_set')
    publication_year = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    copies = models.IntegerField(default=0)
    image = models.ImageField(upload_to='book_images/')
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title} {self.author} {self.publication_year}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Borrow(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    balance_after_borrow = models.DecimalField(default=0, max_digits=12, decimal_places=2,null=True,blank=True)

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.username}"


class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.book.title}"
    
