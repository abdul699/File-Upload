from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
# Create your views here.

#home page view
def home(request):
	context = {}
	members = Account.objects.all()
	count = Account.objects.count()
	context['members'] = members
	context['count'] = count
	return render(request, 'account/home.html', context)

#registration view
def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password) 
			login(request, account)
			return redirect('home')
		#form not valid
		else:
			context['registration_form'] = form
	# GET requets
	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request,'account/register.html', context)



def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect('home')

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect('home')
	else:
		form = AccountAuthenticationForm()
	context['login_form'] = form
	return render(request, 'account/login.html', context)

def update_view(request):
	if not request.user.is_authenticated:
		return redirect('login')
	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = AccountUpdateForm(
			initial={
			"email": request.user.email,
			"username" : request.user.username,
			"first_name" :request.user.first_name,
			})
	context['update_form'] = form
	return render(request, 'account/update.html', context)








