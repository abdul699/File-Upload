from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book
from account.models import Account
# Create your views here.

def upload(request):
	context = {}
	if request.method == 'POST':
		uploaded_file = request.FILES['document']
		fs = FileSystemStorage()
		name = fs.save(uploaded_file.name, uploaded_file)
		u = user.username
		print(u)# u = User.object.get(username)
		context['url'] = fs.url(name)
	return render(request, 'book/upload.html', context)

def book_list(request):
	books = Book.objects.all()
	return render(request, 'book/book_list.html', {
		'books': books,
		})

@login_required
def upload_book(request):
	user = request.user
	if request.method == 'POST':
		form = BookForm(request.POST, request.FILES)
		if form.is_valid():
			obj = form.save(commit=False)
			uploaded_by = Account.objects.filter(email=user.email).first()
			obj.uploaded_by = uploaded_by;
			obj.save()
			return redirect('book_list')
	else:
		form = BookForm()
	return render(request, 'book/upload_book.html', {
		'upload_form' : form
		})