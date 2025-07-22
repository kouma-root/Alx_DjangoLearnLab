from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from .models import Book
from .models import Library
# Create your views here.

def list_books(request):
    books = Book.objects.all()
    context = {'list_books': books}
    return render(request, "relationship_app/list_books.html", context)

class LibraryDetailView(DetailView):
    model = Library
    template_engine = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.get_object() # Access related books
        return context
    
#class register(CreateView):
 #   form_class = UserCreationForm
  #  success_url = reverse_lazy('login')
   # template_name= 'relationship_app/register.html'
   
def register(request):
    form = UserCreationForm()
    return render(request, 'relationship_app/register.html')