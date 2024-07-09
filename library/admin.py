from django.contrib import admin
from .models import Category, Book, Order, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'price')
    search_fields = ('name', 'category__name')
    list_filter = ('category', 'quantity', 'price')
    inlines = [ReviewInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'quantity', 'order_date')
    search_fields = ('user__username', 'book__name')
    list_filter = ('order_date',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'name', 'email', 'body', 'created_on')
    search_fields = ('name', 'email', 'body', 'book__name')
    list_filter = ('created_on',)