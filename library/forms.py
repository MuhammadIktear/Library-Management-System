from django import forms
from .models import Book, Category,Review

class BookForm(forms.ModelForm):
    Category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select())

    class Meta:
        model = Book
        fields = ['image', 'name', 'description', 'quantity', 'price', 'Category']

class ReviewForm(forms.ModelForm):
    class Meta: 
        model = Review
        fields = ['name', 'email', 'body']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })        