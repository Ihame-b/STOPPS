from .models import Cart, Admin, LinfoxUser

def cart_count(request):
    """
    Context processor to add cart item count to all templates
    Returns the total number of items in the cart (sum of all quantities)
    """
    cart_item_count = 0
    cart_id = request.session.get("cart_id", None)
    
    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
            # Count total items (sum of all quantities in cart)
            cart_item_count = sum(cp.quantity for cp in cart.cartproduct_set.all())
        except (Cart.DoesNotExist, ValueError):
            # Cart doesn't exist or invalid cart_id, reset session
            if 'cart_id' in request.session:
                del request.session['cart_id']
            cart_item_count = 0
    
    return {
        'cart_item_count': cart_item_count
    }

def user_permissions(request):
    """
    Context processor to add user permission checks to all templates
    """
    is_admin_user = False
    is_linfox_user = False
    
    if request.user.is_authenticated:
        is_admin_user = Admin.objects.filter(user=request.user).exists()
        is_linfox_user = LinfoxUser.objects.filter(user=request.user).exists()
    
    return {
        'is_admin_user': is_admin_user,
        'is_linfox_user': is_linfox_user
    }
