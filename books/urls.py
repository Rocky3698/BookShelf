from django.urls import path,include
from .views import BookDetail,BorrowBook,PayView,ReturnView
urlpatterns = [
    path('<slug:book_slug>/',BookDetail.as_view(),name='book_details'),
    path('borrow/<slug:book_slug>/',BorrowBook.as_view(),name='borrow_book'),
    path('pay/<slug:book_slug>/',PayView.as_view(),name='pay'),
    path('return/<int:id>/',ReturnView.as_view(),name='return')
]
