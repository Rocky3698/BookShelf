from django.shortcuts import render
from django.views.generic import ListView
from books.models import Book,Category
def home(request):
    return render(request,'home.html')

class Home(ListView):
    template_name = 'home.html'
    context_object_name = 'books'
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug is not None and category_slug != 'all':
            return Book.objects.filter(category__slug=category_slug)
        else:
            return Book.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    
