from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from .models import Category, Product, CartItem, WishlistItem
def home_view(request, slug=None):
    query = request.GET.get('q','')
    products = Product.objects.all()
    categories = Category.objects.all()
    active_category = None
    if slug:
        active_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=active_category)
    if query:
        products = products.filter(Q(name__icontains=query)|Q(description__icontains=query))
    return render(request,'shop/home.html',{'products':products,'categories':categories,'active_category':active_category,'query':query})
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request,'shop/product_detail.html',{'product':product,'related':related})
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1; item.save()
    return redirect('cart')
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user); item.delete(); return redirect('cart')
@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum([i.subtotal() for i in items])
    return render(request,'shop/cart.html',{'items':items,'total':total})
@login_required
def checkout_view(request):
    items = CartItem.objects.filter(user=request.user)
    if request.method=='POST':
        items.delete(); return render(request,'shop/checkout.html',{'success':True})
    total = sum([i.subtotal() for i in items])
    return render(request,'shop/checkout.html',{'items':items,'total':total})
@login_required
def wishlist_view(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request,'shop/wishlist.html',{'items':items})
@login_required
def add_to_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk); WishlistItem.objects.get_or_create(user=request.user, product=product); return redirect('wishlist')
@login_required
def remove_from_wishlist(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk, user=request.user); item.delete(); return redirect('wishlist')
@login_required
def wishlist_move_to_cart(request, pk):
    item = get_object_or_404(WishlistItem, pk=pk, user=request.user)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=item.product)
    if not created: cart_item.quantity += 1; cart_item.save()
    item.delete(); return redirect('cart')
def signup_view(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(); login(request,user); return redirect('home')
    else: form = UserCreationForm()
    return render(request,'shop/signup.html',{'form':form})
def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user(); login(request,user); return redirect('home')
    else: form = AuthenticationForm()
    return render(request,'shop/login.html',{'form':form})
@login_required
def logout_view(request):
    logout(request); return redirect('home')
@login_required
def profile_view(request):
    return render(request,'shop/profile.html')
