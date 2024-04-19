from django.views.generic import DetailView,CreateView
from django.urls import reverse_lazy
from .models import Book
from .models import Review,Borrow,Book
from .forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import date
from django.shortcuts import redirect
from django.views import View
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(user, book, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'book' : book,
            'subject':subject,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

class BookDetail(DetailView,CreateView):
    model = Book
    template_name = 'book_details.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'
    form_class = ReviewForm
    is_borrower = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        categories = book.category.all()
        related_books = Book.objects.none()
        for category in categories:
            related_books |= Book.objects.filter(category=category).exclude(id=book.id)
        context['related_books'] = related_books.distinct()
        context['reviews'] = Review.objects.filter(book=book)
        if Borrow.objects.filter(book=book, borrower=self.request.user).exists():
            self.is_borrower = True
        context['is_borrower'] = self.is_borrower
        return context

    def form_valid(self, form):
        form.instance.book = self.get_object()
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('book_details', kwargs={'book_slug': self.kwargs['book_slug']})
    
class BorrowBook(DetailView):
    template_name = 'borrow.html'
    model = Book
    slug_url_kwarg = 'book_slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['borrower'] = self.request.user
        context['book'] = self.object
        return context


class PayView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book_detail.html' 
    slug_url_kwarg = 'book_slug'
    def get(self, request, *args, **kwargs):
        book = self.get_object()
        account = self.request.user.account
        if book.price>account.balance :
            messages.warning(request,'Insufficiant Balance')
            return redirect('book_details', book_slug=self.kwargs['book_slug'])
        account.balance -= book.price
        account.save()
        book.copies -= 1
        book.save()
        Borrow.objects.create(book=book, borrower=request.user, borrow_date=date.today(),paid_amount=book.price,balance_after_borrow=account.balance)
        messages.success(request, f"You have borrowed '{book.title}' successfully.")
        send_email(self.request.user,book,f'Borrowed Book {book.title}','PaymentMail.html')
        return redirect('book_details', book_slug=self.kwargs['book_slug'])


class ReturnView(View):
    def get(self, request, id):
        try:
            borrow = Borrow.objects.get(pk=id)
            borrow.return_date = datetime.date.today()
            book =borrow.book
            user=borrow.borrower
            user.account.balance += borrow.paid_amount
            borrow.save()
            user.account.save()
            messages.success(request, 'Book returned successfully')
            send_email(self.request.user,book,f'Returned Book {book.title}','ReturnBookMail.html')
            return redirect('profile')
        except Borrow.DoesNotExist:
            messages.warning(request ,'Borrow record not found')
            return redirect('profile')