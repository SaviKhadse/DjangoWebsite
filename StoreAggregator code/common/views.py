from django.shortcuts import render
from product.models import Product, Category
from common.models import *

# Create your views here.
def home_view(request):
    # return HttpResponse('Hello! This is my first PROJECT')
	# return render(request, './home.html')  # Two buttons - Register and Login
	products = Product.objects.all()
	categories = Category.objects.all()

	country = Country.objects.all()
	state = State.objects.all()
	city = City.objects.all()

	return render(request, 'common_html/index.html', {'products':products, 'categories':categories, 'country':country, 'state':state, 'city':city})