import razorpay
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import *
from django.contrib import  messages
from .models import *


# Create your views here.
def home(request):
    return render(request,"home.html")

class CategoryView(View):
    def get(self,request,val):
        art=Art.objects.filter(category=val)
        title = Art.objects.filter(category=val).values('title')
        return render(request,'category.html',locals())

class ProductDetails(View):
    def get(self,request,pk):
        art = Art.objects.get(pk=pk)
        return render(request, 'product-details.html', locals())

def aboutus(request):
    return render(request,'aboutus.html')

def contactus(request):
    return render(request,'contactus.html')





def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user  # Access the user object directly
        art_id = request.GET.get('art_id')
        art = Art.objects.get(id=art_id)
        Cart(user=user, art=art).save()
        return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.art.discount_price
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'addtocart.html', locals())

class CustomerRegister(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'signup.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulation!  User Register Successfully ")
        else:
            messages.warning(request,"Invalid Input Data ")
        return render(request,'signup.html',locals())


class ProfileView(View):
    def get(self, request):
        form=CustomerProfileForm()
        return render(request, 'profile.html', locals())

    def post(self, request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            pincode=form.cleaned_data['pincode']

            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,pincode=pincode)
            reg.save()
            messages.success(request,"Congratulations Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data ")

        return render(request, 'profile.html', locals())
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'address.html', locals())

class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'updateaddress.html', locals())

    def post(self, request, pk):
        forms = CustomerProfileForm(request.POST)
        if forms.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = forms.cleaned_data['name']
            add.locality = forms.cleaned_data['locality']
            add.city = forms.cleaned_data['city']
            add.mobile = forms.cleaned_data['mobile']
            add.state = forms.cleaned_data['state']
            add.pincode = forms.cleaned_data['pincode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')

def plus_cart(request):
    if request.method == 'GET':
        art_id = request.GET.get('art_id')
        if art_id:
            cart = get_object_or_404(Cart, art_id=art_id, user=request.user)
            cart.quantity += 1
            cart.save()
            cart_items = Cart.objects.filter(user=request.user)
            amount = sum(item.quantity * item.art.discount_price for item in cart_items)
            total_amount = amount + 40
            data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': total_amount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'art_id parameter is missing'}, status=400)


def minus_cart(request):
    if request.method == 'GET':
        art_id = request.GET['art_id']
        c = Cart.objects.get(Q(art=art_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.art.discount_price for item in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def remove_cart(request):

    if request.method == 'GET':
        art_id = request.GET['art_id']
        c = Cart.objects.get(Q(art=art_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(item.quantity * item.art.discount_price for item in cart)
        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

class checkout(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.art.discount_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_11"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
            )
            payment.save()
        return render(request, 'checkout.html', locals())

def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, art=c.art, quantity=c.quantity, payment=payment).save()
        c.delete()
    return render(request,"home.html")
def custHome(request):
    return render(request,'home.html')
