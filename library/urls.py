from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
urlpatterns = [
    path('details/<int:pk>/', views.BookDetails.as_view(), name='book_details'),
    path('buy/<int:pk>/', views.buy_book, name='buy_book'),
    path('return/<int:pk>/', views.return_book, name='return_book'),
    path('', views.Book_Category,name='books'),
    path('category/<slug:category_slug>', views.Book_Category,name='category'),    
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)