from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def _get_cart(session):
    return session.setdefault('cart', {})


def _get_or_create_pending_order(user):
    order, created = Order.objects.get_or_create(user=user, status='P', defaults={'total': 0})
    return order

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        order = _get_or_create_pending_order(request.user)
        oi, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': 0})
        oi.quantity += 1
        oi.save()
        return redirect('store:cart')
    cart = _get_cart(request.session)
    cart_item = cart.get(str(product_id), {'quantity':0, 'price': str(product.price)})
    cart_item['quantity'] = cart_item.get('quantity',0) + 1
    cart[str(product_id)] = cart_item
    request.session.modified = True
    return redirect('store:cart')

def cart_remove(request, product_id):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='P').first()
        if order:
            OrderItem.objects.filter(order=order, product_id=product_id).delete()
        return redirect('store:cart')
    cart = _get_cart(request.session)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect('store:cart')

def cart_view(request):
    items = []
    total = Decimal('0')
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='P').first()
        if order:
            for it in order.items.select_related('product').all():
                line_total = it.product.price * it.quantity
                total += line_total
                items.append({'product': it.product, 'quantity': it.quantity, 'line_total': line_total})
    else:
        cart = _get_cart(request.session)
        for pid, data in cart.items():
            try:
                product = Product.objects.get(id=int(pid))
            except Product.DoesNotExist:
                continue
            qty = data.get('quantity', 0)
            line_total = product.price * qty
            total += line_total
            items.append({'product': product, 'quantity': qty, 'line_total': line_total})
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    # If user is authenticated, finalize their pending DB order
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='P').first()
        if not order or not order.items.exists():
            return redirect('store:product_list')
        total = Decimal('0')
        for it in order.items.select_related('product').all():
            total += it.product.price * it.quantity
        order.total = total
        order.status = 'C'
        order.save()
        return redirect(reverse('store:order_success', args=[order.id]))

    # Anonymous checkout: build order from session cart
    cart = _get_cart(request.session)
    if not cart:
        return redirect('store:product_list')
    order = Order.objects.create(user=None)
    total = Decimal('0')
    for pid, data in cart.items():
        product = Product.objects.get(id=int(pid))
        qty = data.get('quantity', 0)
        OrderItem.objects.create(order=order, product=product, quantity=qty)
        total += product.price * qty
    order.total = total
    order.status = 'C'
    order.save()
    request.session['cart'] = {}
    return redirect(reverse('store:order_success', args=[order.id]))


def profile(request):
    if not request.user.is_authenticated:
        return redirect('store:product_list')
    orders = Order.objects.filter(user=request.user).exclude(status='P').order_by('-created_at')
    return render(request, 'store/profile.html', {'orders': orders})


@receiver(user_logged_in)
def merge_session_cart(sender, user, request, **kwargs):
    # When user logs in, merge any session cart into the user's pending order
    session_cart = request.session.get('cart', {})
    if not session_cart:
        return
    order = _get_or_create_pending_order(user)
    for pid, data in session_cart.items():
        try:
            product = Product.objects.get(id=int(pid))
        except Product.DoesNotExist:
            continue
        qty = data.get('quantity', 0)
        if qty <= 0:
            continue
        oi, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': 0})
        oi.quantity += qty
        oi.save()
    # clear session cart after merging
    request.session['cart'] = {}
    request.session.modified = True

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form': form})
