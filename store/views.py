from django.shortcuts import render,redirect
from .models import Product,Order
# Create your views here.

def home(request):
    if 'cart' not in request.session:
        request.session['cart']=[]
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx={'cart':cart,'cart_size':len(cart)}
    return render(request,'store/home.html',ctx)

def storem(request):
    if 'cart' not in request.session:
        request.session['cart']=[]
    cart = request.session['cart']
    request.session.set_expiry(0)
    store_item=Product.objects.all()
    ctx={'store_item':store_item,'cart_size':len(cart)}
    if request.method == "POST":
        cart.append(int(request.POST['obj_id']))
        return redirect('storem')
    return render(request,'store/store.html',ctx)



def cartitem(cart):
    items=[]
    for item in cart:
        items.append(Product.objects.get(id=item))
    return items

def genItemsList(cart):
    cart_item= cartitem(cart)
    items_list=""
    for item in cart_item:
        items_list += str(item.name)
        items_list += ","
    return items_list



def totalcost(cart):
    cart_item=cartitem(cart)
    price=0
    for item in cart_item:
        price += item.price
    return price

def cartview(request):
    
    cart = request.session['cart']
    request.session.set_expiry(0)
    ctx={'cart':cart,'cart_size':len(cart),'cart_item':cartitem(cart),'total':totalcost(cart)}
    return render(request,'store/cart.html',ctx)

def removefromcart(request):
    request.session.set_expiry(0)
    obj_remove=int(request.POST['obj_id'])
    obj_index=request.session['cart'].index(obj_remove)
    request.session['cart'].pop(obj_index)
    return redirect('cartview')

def checkout(request):
    request.session.set_expiry(0)
    cart = request.session['cart']
    ctx={'cart':cart,'cart_size':len(cart),'total':totalcost(cart)}
    return render(request,'store/checkout.html',ctx)

def completeorder(request):
    request.session.set_expiry(0)
    cart = request.session['cart']
    order=Order()
    order.name=request.POST['name']
    order.address=request.POST['address']
    order.phone=request.POST['phone']
    order.payment_method=request.POST['payment']
    order.payment_data=request.POST['payment_data']
    order.item=genItemsList(cart)
    order.save()
    request.session['cart']=[]
    return render(request,'store/complete.html')

def about(request):
    request.session.set_expiry(0)
    cart = request.session['cart']
    ctx={'cart':cart,'cart_size':len(cart)}
    return render(request,'store/about.html',ctx)
