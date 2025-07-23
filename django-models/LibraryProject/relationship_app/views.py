from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required,login_required, user_passes_test
from .utils import is_admin, is_librarian, is_member
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


@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@login_required
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    return render(request, 'relationship_app/book_form.html')


@login_required
@permission_required('relationship_app.can_achange_book', raise_exception=True)
def update_book(request, pk):
    return render(request, 'relationship_app/book_form.html')

@login_required
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    return render(request, 'relationship_app/book_form.html')