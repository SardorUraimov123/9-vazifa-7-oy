from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main import models
import qrcode
from PIL import Image
from io import BytesIO
import base64


def index(request):
    categories = models.Category.objects.all()
    products = []
    reviews = models.Review.objects.all()

    if request.user.is_authenticated:
        liked_products = models.WishList.objects.filter(user=request.user).values_list('product_id', flat=True)
        for product in models.Product.objects.all():
            product.is_like = product.id in liked_products
            products.append(product)
    else:
        products = models.Product.objects.all()

    total_mark = sum(review.mark for review in reviews)
    mark = total_mark // len(reviews) if reviews else 0

    context = {
        'categories': categories,
        'products': products,
        'rating': range(1, 6),
        'mark': mark,
    }
    return render(request, 'front/index.html', context)


def product_detail(request,code):
    product = models.Product.objects.get(code=code)
    reviews = models.Review.objects.filter(product=product)
    images = models.ProductImg.objects.filter(product=product)
    liked = models.WishList.objects.filter(product=product,user=request.user).count() > 0
    mark = 0
    for i in reviews:
        mark += i.mark
    mark = int(mark/len(reviews)) if reviews else 0
    context = {
        'product':product,
        'mark':mark,
        'rating':range(1,6),
        'images':images,
        'reviews':reviews,
        'liked':liked,
    }
    return render(request, 'front/product/detail.html',context)

def product_list(request, code):
    products = []
    categories = models.Category.objects.all()

    if request.user.is_authenticated:
        liked_products = models.WishList.objects.filter(user=request.user).values_list('product_id', flat=True)
        for product in models.Product.objects.filter(category__code=code):
            product.is_like = product.id in liked_products
            products.append(product)
    else:
        products = models.Product.objects.filter(category__code=code)

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'front/category/product_list.html', context)


def product_delete(request,id):
    models.CartProduct.objects.get(id=id).delete()
    return redirect('front:active_cart')


def carts(request):
    queryset = models.Cart.objects.filter(user=request.user, status=4)
    context = {'queryset':queryset}
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:login')
def active_cart(request):
    queryset , _ = models.Cart.objects.get_or_create(user=request.user, status=1)
    return redirect('front:cart_detail', queryset.code)


@login_required(login_url='auth:login')
def cart_detail(request, code):
    cart = models.Cart.objects.get(code=code)
    queryset = models.CartProduct.objects.filter(cart=cart)
    if request.method == 'POST':
        data = list(request.POST.items())[1::]
        for id,value in data:
            cart_product = models.CartProduct.objects.get(id=id)
            cart_product.count = value
            cart_product.product.quantity -= int(value)
            cart.status = 2
            cart_product.product.save()
            cart.save()
            cart_product.save()
    context = {
        'cart': cart,
        'queryset':queryset
        }
    return render(request, 'front/carts/detail.html', context)


def add_to_cart(request,code):
    if models.Product.objects.filter(code=code):
        product = models.Product.objects.get(code=code)
        cart = models.Cart.objects.get(status=1, user=request.user)
        is_product = models.CartProduct.objects.filter(product=product,cart__status=1,cart__user=request.user).first()
        if is_product:
            is_product.count += 1
            is_product.save()
            return redirect('front:active_cart')
        if not cart:
            cart = models.Cart.objects.create(
                user=request.user,
                is_active=True
            )
        models.CartProduct.objects.create(
            product=product,
            cart=cart,
            count=1
        )
        return redirect('front:active_cart')
    return redirect('front:index')


@login_required(login_url='auth:login')
def list_wishlist(request):
    wishlists = models.WishList.objects.filter(user=request.user)
    context = {'wishlists':wishlists,}
    return render(request, 'front/wishlist/list.html',context) 


@login_required(login_url='auth:login')
def remove_wishlist(request,code):
    models.WishList.objects.get(user=request.user,product__code=code).delete()
    return redirect('front:wishlist')


@login_required(login_url='auth:login')
def add_wishlist(request,code):
    product = models.Product.objects.get(code=code)
    wish = models.WishList.objects.filter(product=product,user=request.user)
    if wish.count():
        return redirect('front:remove_wishlist',product.code)
    models.WishList.objects.create(product=product,user= request.user)
    return redirect('front:wishlist')


def order_list(request):
    ordered = models.CartProduct.objects.filter(cart__user=request.user, cart__status=2)
    returned = models.CartProduct.objects.filter(cart__user=request.user, cart__status=3)

    context = {
        'ordered': ordered,
        'returned': returned,
    }
    return render(request, 'front/order/list.html', context)

