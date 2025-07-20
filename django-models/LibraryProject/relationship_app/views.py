from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library
# Create your views here.

def book_list(request):
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, "book/book_list.html", context)

class library_detail(DetailView):
    model = Library
    template_engine = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.get_object() # Access related books
        return context