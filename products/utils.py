from uuid import uuid4

from cart.models import Cart 

def open_session(request):
    if not request.session.get('cart') or not Cart.objects.filter(id=request.session.get('cart')):
        cart = Cart.objects.create()
        request.session['cart'] = str(cart.id)
        request.session['id'] = str(uuid4())