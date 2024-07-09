from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView, TemplateView
from .models import Book, Order, Review, Category
from .forms import BookForm, ReviewForm
from transactions.views import send_transaction_email

@login_required
def buy_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    account = request.user.account
    
    if book.quantity > 0:
        if account.balance >= book.price:
            book.quantity -= 1
            book.save()

            account.balance -= book.price
            account.save()

            Order.objects.create(user=request.user, book=book, quantity=1)
            
            messages.success(request, f'You have successfully borrowed {book.name}!')
            send_transaction_email(request.user, book.price, "Deposit Message", "borrow_email.html")
        else:
            messages.error(request, 'Insufficient balance to borrow this book.')
    else:
        messages.error(request, 'Sorry, this book is out of stock.')
    
    return redirect('book_details', pk=pk)
    
@login_required
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    account = request.user.account
    order = Order.objects.filter(user=request.user, book=book).last()

    if order:
        book.quantity += 1
        book.save()

        account.balance += book.price
        account.save()

        order.delete()
        
        messages.success(request, f'You have successfully returned {book.name}!')
        send_transaction_email(request.user, book.price, "Deposit Message", "returnMoney_email.html")
    else:
        messages.error(request, 'No record of borrowing this book.')
    
    return redirect('user_profile')

class BookDetails(DetailView):
    model = Book
    template_name = 'book_details.html'
    
    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = self.request.user
            new_review.save()
            return redirect('book_details', pk=book.pk)
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form = ReviewForm()
        
        # Check if the user has purchased the book
        user_has_purchased = Order.objects.filter(user=self.request.user, book=book).exists()
        
        context['reviews'] = reviews
        context['review_form'] = review_form
        context['user_has_purchased'] = user_has_purchased
        return context


def Book_Category(request, category_slug=None):
    books = Book.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        books = books.filter(category=category)
    data = Category.objects.all()
    return render(request, 'book.html', {'books': books, 'categories': data})
