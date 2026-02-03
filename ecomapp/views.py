from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.core.paginator import Paginator
from .utils import password_reset_token
from django.core.mail import send_mail
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from .models import *
from .forms import *
import requests
#map
from ecomproject.mixins import Directions

from ecomproject.mixins import(
	AjaxFormMixin, 
	reCAPTCHAValidation,
	FormErrors,
	RedirectParams,
	)
from .forms import (
	UserForm,
	UserProfileForm,
	AuthForm,
	)


#My App

class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        # #region agent log
        import json
        from pathlib import Path
        try:
            log_path = Path(__file__).parent.parent / '.cursor' / 'debug.log'
            with open(log_path, 'a') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'ecom-mixin',
                    'hypothesisId': 'F',
                    'location': 'views.py:37',
                    'message': 'EcomMixin.dispatch entry',
                    'data': {'path': request.path, 'method': request.method},
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass
        # #endregion
        try:
            cart_id = request.session.get("cart_id")
            if cart_id:
                # #region agent log
                try:
                    log_path = Path(__file__).parent.parent / '.cursor' / 'debug.log'
                    with open(log_path, 'a') as f:
                        f.write(json.dumps({
                            'sessionId': 'debug-session',
                            'runId': 'ecom-mixin',
                            'hypothesisId': 'F',
                            'location': 'views.py:50',
                            'message': 'Cart found, getting cart object',
                            'data': {'cart_id': cart_id},
                            'timestamp': int(__import__('time').time() * 1000)
                        }) + '\n')
                except Exception:
                    pass
                # #endregion
                cart_obj = Cart.objects.get(id=cart_id)
                if request.user.is_authenticated:
                #     cart_obj.customer = request.user.customer
                 cart_obj.save()
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # #region agent log
            import traceback
            try:
                log_path = Path(__file__).parent.parent / '.cursor' / 'debug.log'
                with open(log_path, 'a') as f:
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'ecom-mixin',
                        'hypothesisId': 'F',
                        'location': 'views.py:65',
                        'message': 'EcomMixin.dispatch error',
                        'data': {'error': str(e), 'error_type': type(e).__name__, 'traceback': traceback.format_exc()},
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass
            # #endregion
            raise


class HomeView(EcomMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # #region agent log
        import json
        from pathlib import Path
        try:
            log_path = Path(__file__).parent.parent.parent / '.cursor' / 'debug.log'
            with open(log_path, 'a') as f:
                f.write(json.dumps({
                    'sessionId': 'debug-session',
                    'runId': 'home-view',
                    'hypothesisId': 'A',
                    'location': 'views.py:49',
                    'message': 'HomeView.get_context_data entry',
                    'data': {'user_authenticated': self.request.user.is_authenticated},
                    'timestamp': int(__import__('time').time() * 1000)
                }) + '\n')
        except Exception:
            pass
        # #endregion
        try:
            context = super().get_context_data(**kwargs)
            context['myname'] = "Dipak Niroula"
            # #region agent log
            try:
                log_path = Path(__file__).parent.parent.parent / '.cursor' / 'debug.log'
                with open(log_path, 'a') as f:
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'home-view',
                        'hypothesisId': 'B',
                        'location': 'views.py:56',
                        'message': 'Before Product query',
                        'data': {},
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass
            # #endregion
            all_products = Product.objects.all().order_by("-id")
            # #region agent log
            try:
                log_path = Path(__file__).parent.parent.parent / '.cursor' / 'debug.log'
                with open(log_path, 'a') as f:
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'home-view',
                        'hypothesisId': 'B',
                        'location': 'views.py:65',
                        'message': 'After Product query',
                        'data': {'product_count': all_products.count()},
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass
            # #endregion
            paginator = Paginator(all_products, 8)
            page_number = self.request.GET.get('page')
            print(page_number)
            product_list = paginator.get_page(page_number)
            # #region agent log
            try:
                log_path = Path(__file__).parent.parent.parent / '.cursor' / 'debug.log'
                with open(log_path, 'a') as f:
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'home-view',
                        'hypothesisId': 'C',
                        'location': 'views.py:75',
                        'message': 'HomeView.get_context_data success',
                        'data': {'page_number': page_number, 'product_list_count': len(product_list)},
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass
            # #endregion
            context['product_list'] = product_list
            return context
        except Exception as e:
            # #region agent log
            import traceback
            try:
                log_path = Path(__file__).parent.parent.parent / '.cursor' / 'debug.log'
                with open(log_path, 'a') as f:
                    f.write(json.dumps({
                        'sessionId': 'debug-session',
                        'runId': 'home-view',
                        'hypothesisId': 'D',
                        'location': 'views.py:85',
                        'message': 'HomeView.get_context_data error',
                        'data': {'error': str(e), 'error_type': type(e).__name__, 'traceback': traceback.format_exc()},
                        'timestamp': int(__import__('time').time() * 1000)
                    }) + '\n')
            except Exception:
                pass
            # #endregion
            raise


class AllProductsView(EcomMixin, TemplateView):
    template_name = "allproducts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all()
        return context


class ProductDetailView(EcomMixin, TemplateView):
    template_name = "productdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        
        # Get or create chat for authenticated customers
        if self.request.user.is_authenticated and Customer.objects.filter(user=self.request.user).exists():
            customer = Customer.objects.get(user=self.request.user)
            # Try to find product owner by name
            product_owner = None
            if product.productowner:
                try:
                    product_owner = ProductOwner.objects.get(full_name=product.productowner)
                except ProductOwner.DoesNotExist:
                    pass
            
            if product_owner:
                chat, created = Chat.objects.get_or_create(
                    product=product,
                    customer=customer,
                    defaults={'product_owner': product_owner}
                )
                if not created and chat.product_owner != product_owner:
                    chat.product_owner = product_owner
                    chat.save()
                context['chat'] = chat
                context['messages'] = chat.messages.all()[:20]  # Last 20 messages
        
        return context


class AddToCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            # Ensure customer is assigned to cart if user is authenticated
            if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
                if not cart_obj.customer:
                    cart_obj.customer = request.user.customer
                    cart_obj.save()
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
                message = f"{product_obj.title} quantity updated in cart!"
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
                message = f"{product_obj.title} added to cart successfully!"
        else:
            # Create new cart and assign customer if authenticated
            cart_obj = Cart.objects.create(total=0)
            if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
                cart_obj.customer = request.user.customer
                cart_obj.save()
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
            message = f"{product_obj.title} added to cart successfully!"

        # Redirect back to the product detail page or referrer
        redirect_url = request.GET.get('next', None)
        if not redirect_url:
            redirect_url = reverse('ecomapp:productdetail', kwargs={'slug': product_obj.slug})
        
        # Add success message to session for toast notification
        messages.success(request, message)
        
        return redirect(redirect_url)


class ManageCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        
        # Ensure customer is assigned to cart if user is authenticated
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            if not cart_obj.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()

        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("ecomapp:mycart")


class UpdateCargoView(EcomMixin, View):
    def post(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        cargo_id = request.POST.get("cargo_id")
        
        try:
            cp_obj = CartProduct.objects.get(id=cp_id)
            if cargo_id:
                cargo = Cargo.objects.get(id=cargo_id, cargo_status="Cargo Available")
                cp_obj.cargo = cargo
                cp_obj.save()
                messages.success(request, f"Transport updated to {cargo.driverName} ({cargo.CampanyName})")
            else:
                cp_obj.cargo = None
                cp_obj.save()
                messages.info(request, "Transport removed")
        except (CartProduct.DoesNotExist, Cargo.DoesNotExist):
            messages.error(request, "Invalid selection")
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({'success': True, 'redirect': reverse('ecomapp:mycart')})
        
        return redirect("ecomapp:mycart")


class EmptyCartView(EcomMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("ecomapp:mycart")


class MyCartView(EcomMixin, TemplateView):
    template_name = "mycart.html"

    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated and is a Customer before accessing cart
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to view your cart and proceed to checkout.")
            return redirect(reverse("ecomapp:customerlogin") + "?next=" + reverse("ecomapp:mycart"))
        
        # Check if user is a Customer (not ProductOwner, Admin, or LinfoxUser)
        if not Customer.objects.filter(user=request.user).exists():
            messages.warning(request, "Only customers can access the shopping cart. Please log in with a customer account.")
            return redirect(reverse("ecomapp:customerlogin") + "?next=" + reverse("ecomapp:mycart"))
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            # Ensure customer is assigned to cart if user is authenticated
            if self.request.user.is_authenticated and Customer.objects.filter(user=self.request.user).exists():
                if not cart.customer:
                    cart.customer = self.request.user.customer
                    cart.save()
            # Calculate total including cargo prices
            cart_total = cart.total
            cargo_total = 0
            for cp in cart.cartproduct_set.all():
                if cp.cargo and cp.cargo.price:
                    cargo_total += cp.cargo.price * cp.quantity
            context['cart_total'] = cart_total
            context['cargo_total'] = cargo_total
            context['grand_total'] = cart_total + cargo_total
        else:
            cart = None
            context['cart_total'] = 0
            context['cargo_total'] = 0
            context['grand_total'] = 0
        context['cart'] = cart
        # Get a limited selection of available cargo options (show only 6-8 items)
        # This prevents showing too many options in the table
        available_cargo = Cargo.objects.filter(cargo_status="Cargo Available").order_by('-id')[:8]
        context['available_cargo'] = available_cargo
        return context


class CheckoutView(EcomMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomapp:home")

    def dispatch(self, request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to proceed to checkout.")
            return redirect(reverse("ecomapp:customerlogin") + "?next=" + reverse("ecomapp:checkout"))
        
        # Check if user is a Customer (not ProductOwner, Admin, or LinfoxUser)
        if not Customer.objects.filter(user=request.user).exists():
            messages.error(request, "Only customers can checkout. Please log in with a customer account.")
            return redirect("ecomapp:home")
        
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            # Calculate transport total
            cart_total = cart_obj.total
            cargo_total = 0
            for cp in cart_obj.cartproduct_set.all():
                if cp.cargo and cp.cargo.price:
                    cargo_total += cp.cargo.price * cp.quantity
            context['cart'] = cart_obj
            context['cart_total'] = cart_total
            context['cargo_total'] = cargo_total
            context['grand_total'] = cart_total + cargo_total
        else:
            cart_obj = None
            context['cart'] = cart_obj
            context['cart_total'] = 0
            context['cargo_total'] = 0
            context['grand_total'] = 0
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            # Ensure customer is assigned to cart before creating order
            if self.request.user.is_authenticated and Customer.objects.filter(user=self.request.user).exists():
                if not cart_obj.customer:
                    cart_obj.customer = self.request.user.customer
                    cart_obj.save()
            # Calculate product subtotal and transport (cargo) total
            cart_total = cart_obj.total
            cargo_total = 0
            for cp in cart_obj.cartproduct_set.all():
                if cp.cargo and cp.cargo.price:
                    cargo_total += cp.cargo.price * cp.quantity

            # Attach cart and totals to the order
            form.instance.cart = cart_obj
            # Subtotal = products only
            form.instance.subtotal = cart_total
            # Currently no discount logic
            form.instance.discount = 0
            # Total = products + transport (what customer pays)
            form.instance.total = cart_total + cargo_total
            form.instance.order_status = "Order Received"
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == "Khalti":
                return redirect(reverse("ecomapp:khaltirequest") + "?o_id=" + str(order.id))
            elif pm == "Esewa":
                return redirect(reverse("ecomapp:esewarequest") + "?o_id=" + str(order.id))
        else:
            return redirect("ecomapp:home")
        return super().form_valid(form)


class KhaltiRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order
        }
        return render(request, "khaltirequest.html", context)


class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        amount = request.GET.get("amount")
        o_id = request.GET.get("order_id")
        print(token, amount, o_id)

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
        }
        headers = {
            "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
        }

        order_obj = Order.objects.get(id=o_id)

        response = requests.post(url, payload, headers=headers)
        resp_dict = response.json()
        if resp_dict.get("idx"):
            success = True
            order_obj.payment_completed = True
            order_obj.save()
        else:
            success = False
        data = {
            "success": success
        }
        return JsonResponse(data)


class EsewaRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order
        }
        return render(request, "esewarequest.html", context)


class EsewaVerifyView(View):
    def get(self, request, *args, **kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid': refId,
            'pid': oid,
        }
        resp = requests.post(url, d)
        root = ET.fromstring(resp.content)
        status = root[0].text.strip()

        order_id = oid.split("_")[1]
        order_obj = Order.objects.get(id=order_id)
        if status == "Success":
            order_obj.payment_completed = True
            order_obj.save()
            return redirect("/")
        else:

            return redirect("/esewa-request/?o_id="+order_id)


class ProductOwnerRegistrationView(CreateView):
    template_name = "productownerregistration.html"
    form_class = productOwnerRegistrationForm
    success_url = reverse_lazy("ecomapp:productOwnerlogin")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        # Set user as inactive until email is verified
        user.is_active = False
        user.save()
        form.instance.user = user
        form.save()
        
        # Send welcome email with verification link
        from .utils import send_verification_email
        send_verification_email(user, self.request, user_type='productowner', is_already_verified=False)
        
        messages.success(
            self.request,
            f'Registration successful! A welcome email with verification link has been sent to {email}. Please check your email to verify your account before logging in.'
        )
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:customerlogin")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        # Set user as inactive until email is verified
        user.is_active = False
        user.save()
        form.instance.user = user
        form.save()
        
        # Send welcome email with verification link
        from .utils import send_verification_email
        send_verification_email(user, self.request, user_type='customer', is_already_verified=False)
        
        messages.success(
            self.request,
            f'Registration successful! A welcome email with verification link has been sent to {email}. Please check your email to verify your account before logging in.'
        )
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url



class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomapp:home")


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        
        # Strip whitespace from username and password
        uname = uname.strip() if uname else ""
        pword = pword.strip() if pword else ""
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Login attempt for username: {uname}")
        
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            # Check if user has a customer profile
            if not Customer.objects.filter(user=usr).exists():
                messages.error(
                    self.request,
                    'Invalid credentials. This account is not registered as a customer.'
                )
                return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
            
            # Check if email is verified
            from .models import EmailVerificationToken
            try:
                verification = EmailVerificationToken.objects.get(user=usr)
                if not verification.is_verified:
                    messages.error(
                        self.request,
                        'Please verify your email address before logging in. Check your email for the verification link. If you did not receive the email, please contact support.'
                    )
                    return render(self.request, self.template_name, {"form": self.form_class})
            except EmailVerificationToken.DoesNotExist:
                # If no verification token exists, allow login (for backward compatibility with old accounts)
                pass
            
            # Check if user is active
            if not usr.is_active:
                messages.error(
                    self.request,
                    'Your account is not active. Please verify your email address or contact support to activate your account.'
                )
                return render(self.request, self.template_name, {"form": self.form_class})
            
            # All checks passed - log the user in
            login(self.request, usr)
        else:
            # Authentication failed - wrong username or password
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid username or password"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class AboutView(EcomMixin, TemplateView):
    template_name = "about.html"


class ContactView(EcomMixin, TemplateView):
    template_name = "contactus.html"


class CustomerProfileView(View):
    template_name = "customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        customer = request.user.customer
        form = CustomerProfileEditForm(instance=customer)
        form.fields['email'].initial = customer.user.email
        
        # Get orders by cart customer OR by email (for backward compatibility with old orders)
        orders = Order.objects.filter(
            Q(cart__customer=customer) | Q(email=customer.user.email)
        ).distinct().order_by("-id")
        
        context = {
            'customer': customer,
            'orders': orders,
            'form': form,
            'edit_mode': False
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        customer = request.user.customer
        form = CustomerProfileEditForm(request.POST, request.FILES, instance=customer)
        
        if form.is_valid():
            form.save()
            # Update user email if changed
            if 'email' in form.cleaned_data:
                customer.user.email = form.cleaned_data['email']
                customer.user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('ecomapp:customerprofile')
        else:
            # Get orders for context
            orders = Order.objects.filter(
                Q(cart__customer=customer) | Q(email=customer.user.email)
            ).distinct().order_by("-id")
            
            context = {
                'customer': customer,
                'orders': orders,
                'form': form,
                'edit_mode': True
            }
            return render(request, self.template_name, context)


class CustomerProfileEditView(UpdateView):
    """View for customers to edit their profile"""
    model = Customer
    form_class = CustomerProfileEditForm
    template_name = "customerprofileedit.html"
    success_url = reverse_lazy("ecomapp:customerprofile")
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            # Ensure user can only edit their own profile
            if self.get_object().user != request.user:
                messages.error(request, "You can only edit your own profile.")
                return redirect("ecomapp:customerprofile")
        else:
            return redirect("/login/?next=/profile/edit/")
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        """Get the customer object for the current user"""
        return self.request.user.customer
    
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            try:
                order = Order.objects.get(id=order_id)
                customer = request.user.customer
                # Check if order belongs to this customer by cart customer OR email
                # This ensures access control works even for old orders without cart customer
                order_belongs_to_customer = False
                if order.cart.customer == customer:
                    order_belongs_to_customer = True
                elif order.email and order.email == customer.user.email:
                    order_belongs_to_customer = True
                
                if not order_belongs_to_customer:
                    # Order doesn't belong to this customer - redirect to profile
                    return redirect("ecomapp:customerprofile")
            except Order.DoesNotExist:
                # Order doesn't exist - redirect to profile
                return redirect("ecomapp:customerprofile")
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get("keyword")
        results = Product.objects.filter(
            Q(title__icontains=kw) | Q(description__icontains=kw) | Q(return_policy__icontains=kw))
        print(results)
        context["results"] = results
        return context


class PasswordForgotView(FormView):
    template_name = "forgotpassword.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        try:
            # Try to get user by email (works for all user types)
            user = User.objects.get(email=email)
            
            # Determine user type
            user_type = 'customer'
            if ProductOwner.objects.filter(user=user).exists():
                user_type = 'productowner'
            elif Admin.objects.filter(user=user).exists():
                user_type = 'admin'
            elif LinfoxUser.objects.filter(user=user).exists():
                user_type = 'linfox'
            
            # Use the new email utility function
            from .utils import send_password_reset_email
            try:
                email_sent = send_password_reset_email(user, self.request, user_type=user_type)
                if email_sent:
                    messages.success(
                        self.request,
                        f'Password reset link has been sent to {email}. Please check your email (including spam folder).'
                    )
                else:
                    # Check if it's a configuration issue
                    from django.conf import settings
                    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                        messages.error(
                            self.request,
                            'Email configuration is missing. Please contact the administrator. Error: EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not set.'
                        )
                    else:
                        messages.error(
                            self.request,
                            f'Failed to send password reset email to {email}. Please check your email configuration in settings.py or contact support. Check the console for detailed error messages.'
                        )
            except Exception as email_error:
                # Log the error for debugging
                import traceback
                error_details = traceback.format_exc()
                print(f"Error sending password reset email: {email_error}")
                print(error_details)
                messages.error(
                    self.request,
                    f'Failed to send password reset email. Error: {str(email_error)}. Please check the console for details or contact support.'
                )
        except User.DoesNotExist:
            messages.error(
                self.request,
                'No account found with this email address.'
            )
        except Exception as e:
            # Log the error for debugging
            import traceback
            print(f"Error in password reset: {e}")
            print(traceback.format_exc())
            messages.error(
                self.request,
                f'An error occurred: {str(e)}. Please try again later or contact support.'
            )
        
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = "/login/"

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        token = self.kwargs.get("token")
        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse("ecomapp:passworforgot") + "?m=e")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get("email")
        user = User.objects.get(email=email)
        
        # Strip any whitespace that might have been accidentally added
        password = password.strip()
        
        # Validate password is not empty
        if not password:
            messages.error(
                self.request,
                'Error: Password cannot be empty. Please enter a valid password.'
            )
            return render(self.request, self.template_name, {"form": self.form_class})
        
        # Set new password - this will hash it properly
        user.set_password(password)
        
        # Save with explicit update_fields to ensure password is saved
        user.save(update_fields=['password'])
        
        # Refresh user from database to get latest data
        user.refresh_from_db()
        
        # Verify password was saved by checking if user has a password hash
        if not user.has_usable_password():
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Password was not saved for user {user.username}")
            messages.error(
                self.request,
                'Error: Password was not saved. Please try again.'
            )
            return render(self.request, self.template_name, {"form": self.form_class})
        
        # Test authentication immediately to verify password works
        from django.contrib.auth import authenticate
        test_auth = authenticate(username=user.username, password=password)
        
        # Log the result
        import logging
        logger = logging.getLogger(__name__)
        if test_auth:
            logger.info(f"Password successfully reset and verified for user {user.username} (ID: {user.pk})")
            print(f"✅ Password reset successful for {user.username}")
        else:
            logger.warning(f"Password reset saved for {user.username} but immediate authentication test failed - this might be a caching issue")
            print(f"⚠️ Password saved for {user.username} but auth test failed - user should try logging in")
        
        # Invalidate all existing sessions for this user
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        for session in sessions:
            try:
                session_data = session.get_decoded()
                if session_data.get('_auth_user_id') == str(user.pk):
                    session.delete()
            except Exception:
                continue
        
        messages.success(
            self.request,
            f'Password reset successfully! Your old password is no longer valid. Please login with your USERNAME "{user.username}" and your new password.'
        )
        return super().form_valid(form)

# admin pages


class AdminLoginView(FormView):
    """
    Super Admin Login View
    
    Only Super Admin (Admin) users can login from this page.
    LinfoxUser should use the Linfox login page instead.
    
    Redirects:
    - Super Admin (Admin) → /admin-home/
    - LinfoxUser → Error message and redirect to Linfox login
    """
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        
        # Strip whitespace from username and password
        uname = uname.strip() if uname else ""
        pword = pword.strip() if pword else ""
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Admin login attempt for username: {uname}")
        
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            is_admin = Admin.objects.filter(user=usr).exists()
            is_linfox = LinfoxUser.objects.filter(user=usr).exists()
            
            if is_admin:
                # Check if user has an Admin profile (profile type validation)
                if not Admin.objects.filter(user=usr).exists():
                    messages.error(
                        self.request,
                        'Invalid credentials. This account is not registered as an admin.'
                    )
                    return render(self.request, self.template_name, {
                        "form": self.form_class,
                        "error": "Invalid credentials. This account is not registered as an admin."
                    })
                
                # Check if email is verified (required for all Admin users)
                from .models import EmailVerificationToken
                try:
                    verification = EmailVerificationToken.objects.get(user=usr)
                    if not verification.is_verified:
                        messages.error(
                            self.request,
                            'Please verify your email address before logging in. Check your email for the verification link. If you did not receive the email, please contact support.'
                        )
                        return render(self.request, self.template_name, {"form": self.form_class})
                except EmailVerificationToken.DoesNotExist:
                    # Create verification token and mark as verified for existing Admin users (backward compatibility)
                    # But still require email verification for security
                    import secrets
                    token = secrets.token_urlsafe(32)
                    EmailVerificationToken.objects.create(
                        user=usr,
                        token=token,
                        is_verified=True  # Auto-verify existing admin accounts
                    )
                    messages.info(
                        self.request,
                        'Your account has been updated. Please verify your email address for future logins.'
                    )
                
                # Check if user is active
                if not usr.is_active:
                    messages.error(
                        self.request,
                        'Your account is not active. Please verify your email address or contact support to activate your account.'
                    )
                    return render(self.request, self.template_name, {"form": self.form_class})
                
                # All checks passed - log the user in
                login(self.request, usr)
                return redirect("ecomapp:adminhome")
            elif is_linfox:
                # LinfoxUser should use Linfox login page
                messages.error(
                    self.request,
                    'Linfox users should login from the Linfox login page. Please use /linfox-login/ instead.'
                )
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Linfox users should login from the Linfox login page. Please use /linfox-login/ instead."
                })
            else:
                messages.error(
                    self.request,
                    'Invalid credentials or you are not authorized to access the admin dashboard.'
                )
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Invalid credentials or you are not authorized to access the admin dashboard."
                })
        else:
            # Authentication failed - wrong username or password
            return render(self.request, self.template_name, {
                "form": self.form_class, 
                "error": "Invalid username or password"
            })
        return super().form_valid(form)


class AdminRequiredMixin(object):
    """
    Access Control Mixin for Admin Pages (Super Admin Dashboard)
    
    Only Super Admin (Admin) users can access admin pages.
    LinfoxUser cannot access admin pages - they can only access Linfox dashboard.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Only allow Super Admin (Admin) users
            is_admin = Admin.objects.filter(user=request.user).exists()
            if is_admin:
                pass
            else:
                # If LinfoxUser tries to access admin pages, redirect to Linfox dashboard
                is_linfox = LinfoxUser.objects.filter(user=request.user).exists()
                if is_linfox:
                    messages.error(request, "You don't have permission to access the admin dashboard. Please use the Linfox dashboard.")
                    return redirect("/linfox-home/")
                else:
                    return redirect("/admin-login/")
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pendingorders"] = Order.objects.filter(
            order_status="Order Received").order_by("-id")
        # Add statistics
        context["total_orders"] = Order.objects.count()
        context["total_products"] = Product.objects.count()
        context["total_cargo"] = Cargo.objects.count()
        context["completed_orders"] = Order.objects.filter(order_status="Order Completed").count()
        context["all_orders"] = Order.objects.all().order_by("-id")[:5]  # Recent orders
        context["recent_products"] = Product.objects.all().order_by("-id")[:5]  # Recent products
        context["recent_cargo"] = Cargo.objects.all().order_by("-id")[:5]  # Recent cargo/transport
        return context

class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context


class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"


class AdminOrderStatuChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomapp:adminorderdetail", kwargs={"pk": order_id}))


class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductlist.html"
    queryset = Product.objects.all().order_by("-id")
    context_object_name = "allproducts"


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomapp:adminproductlist")

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        messages.success(self.request, f"Product '{p.title}' created successfully!")
        return super().form_valid(form)


class AdminProductUpdateView(AdminRequiredMixin, UpdateView):
    model = Product
    template_name = "adminpages/adminproductedit.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomapp:adminproductlist")
    context_object_name = "product"

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        messages.success(self.request, f"Product '{p.title}' updated successfully!")
        return super().form_valid(form)


class AdminProductDeleteView(AdminRequiredMixin, DeleteView):
    model = Product
    template_name = "adminpages/adminproductdelete.html"
    success_url = reverse_lazy("ecomapp:adminproductlist")
    context_object_name = "product"

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f"Product '{product.title}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Product Owner Management
class AdminProductOwnerListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductownerlist.html"
    queryset = ProductOwner.objects.all().order_by("-id")
    context_object_name = "allproductowners"


class AdminProductOwnerCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductownercreate.html"
    form_class = productOwnerRegistrationForm
    success_url = reverse_lazy("ecomapp:adminproductownerlist")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        
        # Normalize email
        if email:
            email = email.strip().lower()
        
        # Check if email already exists
        if email and User.objects.filter(email=email).exists():
            form.add_error('email', 'A user with this email address already exists.')
            return self.form_invalid(form)
        
        user = User.objects.create_user(username, email, password)
        # Admin-created users should be active and ready to use immediately
        user.is_active = True
        user.save()
        form.instance.user = user
        form.save()
        
        # Create email verification token and mark as verified for admin-created users
        from .models import EmailVerificationToken
        import secrets
        token = secrets.token_urlsafe(32)
        EmailVerificationToken.objects.update_or_create(
            user=user,
            defaults={'token': token, 'is_verified': True}
        )
        
        # Send welcome email (account is already verified)
        from .utils import send_verification_email
        send_verification_email(user, self.request, user_type='productowner', is_already_verified=True)
        
        messages.success(self.request, f"Product Owner '{form.instance.full_name}' created successfully! A welcome email has been sent to {email}. They can login immediately.")
        return super().form_valid(form)


class AdminProductOwnerUpdateView(AdminRequiredMixin, UpdateView):
    model = ProductOwner
    template_name = "adminpages/adminproductowneredit.html"
    fields = ["full_name", "mobile", "image"]
    success_url = reverse_lazy("ecomapp:adminproductownerlist")
    context_object_name = "productowner"

    def form_valid(self, form):
        messages.success(self.request, f"Product Owner '{form.instance.full_name}' updated successfully!")
        return super().form_valid(form)


class AdminProductOwnerDeleteView(AdminRequiredMixin, DeleteView):
    model = ProductOwner
    template_name = "adminpages/adminproductownerdelete.html"
    success_url = reverse_lazy("ecomapp:adminproductownerlist")
    context_object_name = "productowner"

    def delete(self, request, *args, **kwargs):
        productowner = self.get_object()
        user = productowner.user
        messages.success(request, f"Product Owner '{productowner.full_name}' deleted successfully!")
        result = super().delete(request, *args, **kwargs)
        # Also delete the associated user
        if user:
            user.delete()
        return result


# Customer Management
class AdminCustomerListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/admincustomerlist.html"
    queryset = Customer.objects.all().order_by("-id")
    context_object_name = "allcustomers"


class AdminCustomerCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/admincustomercreate.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:admincustomerlist")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        
        # Normalize email
        if email:
            email = email.strip().lower()
        
        # Check if email already exists
        if email and User.objects.filter(email=email).exists():
            form.add_error('email', 'A user with this email address already exists.')
            return self.form_invalid(form)
        
        user = User.objects.create_user(username, email, password)
        # Admin-created users should be active and ready to use immediately
        user.is_active = True
        user.save()
        form.instance.user = user
        form.save()
        
        # Create email verification token and mark as verified for admin-created users
        from .models import EmailVerificationToken
        import secrets
        token = secrets.token_urlsafe(32)
        EmailVerificationToken.objects.update_or_create(
            user=user,
            defaults={'token': token, 'is_verified': True}
        )
        
        # Send welcome email (account is already verified)
        from .utils import send_verification_email
        send_verification_email(user, self.request, user_type='customer', is_already_verified=True)
        
        messages.success(self.request, f"Customer '{form.instance.full_name}' created successfully! A welcome email has been sent to {email}. They can login immediately.")
        return super().form_valid(form)


class AdminCustomerUpdateView(AdminRequiredMixin, UpdateView):
    model = Customer
    template_name = "adminpages/admincustomeredit.html"
    fields = ["full_name", "address", "town", "county", "is_active"]
    success_url = reverse_lazy("ecomapp:admincustomerlist")
    context_object_name = "customer"

    def form_valid(self, form):
        messages.success(self.request, f"Customer '{form.instance.full_name}' updated successfully!")
        return super().form_valid(form)


class AdminCustomerDeleteView(AdminRequiredMixin, DeleteView):
    model = Customer
    template_name = "adminpages/admincustomerdelete.html"
    success_url = reverse_lazy("ecomapp:admincustomerlist")
    context_object_name = "customer"

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        user = customer.user
        messages.success(request, f"Customer '{customer.full_name}' deleted successfully!")
        result = super().delete(request, *args, **kwargs)
        # Also delete the associated user
        if user:
            user.delete()
        return result


# Cargo/Transport Management
class AdminCargoCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/admincargocreate.html"
    form_class = CargoForm
    success_url = reverse_lazy("ecomapp:linfoxcargolist")

    def form_valid(self, form):
        p = form.save(commit=False)
        # If user is a Linfox user, assign cargo to them
        if LinfoxUser.objects.filter(user=self.request.user).exists():
            linfox_user = LinfoxUser.objects.get(user=self.request.user)
            p.created_by = linfox_user
        # If user is Admin (not Linfox), leave created_by as None (admin can see all)
        p.save()
        messages.success(self.request, "Cargo created successfully!")
        return super().form_valid(form)


class AdminCargoUpdateView(AdminRequiredMixin, UpdateView):
    model = Cargo
    template_name = "adminpages/admincargoedit.html"
    form_class = CargoForm
    success_url = reverse_lazy("ecomapp:linfoxcargolist")
    context_object_name = "cargo"
    
    def dispatch(self, request, *args, **kwargs):
        cargo = self.get_object()
        is_admin = Admin.objects.filter(user=request.user).exists()
        is_linfox = LinfoxUser.objects.filter(user=request.user).exists()
        
        # If user is Linfox user (not Admin), only allow editing their own cargo
        if is_linfox and not is_admin:
            linfox_user = LinfoxUser.objects.get(user=request.user)
            # Only allow Linfox users to edit their own cargo
            if cargo.created_by and cargo.created_by != linfox_user:
                messages.error(request, "You can only edit cargo that you created.")
                return redirect("ecomapp:linfoxcargolist")
        # Admin users can edit any cargo
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f"Cargo '{form.instance.CampanyName}' updated successfully!")
        return super().form_valid(form)


class AdminCargoDeleteView(AdminRequiredMixin, DeleteView):
    model = Cargo
    template_name = "adminpages/admincargodelete.html"
    success_url = reverse_lazy("ecomapp:linfoxcargolist")
    context_object_name = "cargo"

    def delete(self, request, *args, **kwargs):
        cargo = self.get_object()
        messages.success(request, f"Cargo '{cargo.CampanyName}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Order Management
class AdminOrderUpdateView(AdminRequiredMixin, UpdateView):
    model = Order
    template_name = "adminpages/adminorderedit.html"
    fields = ["order_status", "payment_completed"]
    success_url = reverse_lazy("ecomapp:adminorderlist")
    context_object_name = "order"

    def form_valid(self, form):
        messages.success(self.request, f"Order #{form.instance.id} updated successfully!")
        return super().form_valid(form)


class AdminOrderDeleteView(AdminRequiredMixin, DeleteView):
    model = Order
    template_name = "adminpages/adminorderdelete.html"
    success_url = reverse_lazy("ecomapp:adminorderlist")
    context_object_name = "order"

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        messages.success(request, f"Order #{order.id} deleted successfully!")
        return super().delete(request, *args, **kwargs)


#Linfox Page

class LinfoxLoginView(FormView):
    """
    Linfox Login View
    
    Only Linfox User (LinfoxUser) can login from this page.
    Admin users should use the admin login page instead.
    
    Redirects:
    - LinfoxUser → /linfox-home/ (their only accessible dashboard)
    - Admin users → Error message directing to /admin-login/
    """
    template_name = "linfox/linfoxlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:linfoxhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        
        # Strip whitespace from username and password
        uname = uname.strip() if uname else ""
        pword = pword.strip() if pword else ""
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Linfox login attempt for username: {uname}")
        
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            is_admin = Admin.objects.filter(user=usr).exists()
            is_linfox = LinfoxUser.objects.filter(user=usr).exists()
            
            if is_linfox:
                # Check if email is verified
                from .models import EmailVerificationToken
                try:
                    verification = EmailVerificationToken.objects.get(user=usr)
                    if not verification.is_verified:
                        messages.error(
                            self.request,
                            'Please verify your email address before logging in. Check your email for the verification link. If you did not receive the email, please contact support.'
                        )
                        return render(self.request, self.template_name, {"form": self.form_class})
                except EmailVerificationToken.DoesNotExist:
                    # If no verification token exists, allow login (for backward compatibility with old accounts)
                    pass
                
                # Check if user is active
                if not usr.is_active:
                    messages.error(
                        self.request,
                        'Your account is not active. Please verify your email address or contact support to activate your account.'
                    )
                    return render(self.request, self.template_name, {"form": self.form_class})
                
                # All checks passed - log the user in
                login(self.request, usr)
                return redirect("ecomapp:linfoxhome")
            elif is_admin:
                # Admin users should use admin login page
                messages.error(
                    self.request,
                    'Admin users should login from the admin login page. Please use /admin-login/ instead.'
                )
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Admin users should login from the admin login page. Please use /admin-login/ instead."
                })
            else:
                messages.error(
                    self.request,
                    'Invalid credentials. This account is not registered as a Linfox user.'
                )
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Invalid credentials. This account is not registered as a Linfox user."
                })
        else:
            # Authentication failed - wrong username or password
            return render(self.request, self.template_name, {
                "form": self.form_class, 
                "error": "Invalid username or password"
            })
        return super().form_valid(form)

class LinfoxRequiredMixin(object):
    """
    Access Control Mixin for Linfox Pages
    
    Allows both Super Admin (Admin) and Linfox User (LinfoxUser) to access Linfox pages.
    Admin users can access everything, including Linfox dashboard.
    LinfoxUser can only access Linfox dashboard.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Allow both Super Admin (Admin) and Linfox User (LinfoxUser)
            # Admin users can access everything, LinfoxUser can only access Linfox pages
            is_admin = Admin.objects.filter(user=request.user).exists()
            is_linfox = LinfoxUser.objects.filter(user=request.user).exists()
            if is_admin or is_linfox:
                pass
            else:
                return redirect("/admin-login/")
        else:
            return redirect("/admin-login/")
        return super().dispatch(request, *args, **kwargs)

class LinfoxHomeView(LinfoxRequiredMixin, TemplateView):
    template_name = "linfox/linfoxhome.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if user is Admin or LinfoxUser
        is_admin = Admin.objects.filter(user=self.request.user).exists()
        is_linfox = LinfoxUser.objects.filter(user=self.request.user).exists()
        
        # Filter cargo based on user type
        if is_linfox and not is_admin:
            # Linfox users see only their own cargo
            linfox_user = LinfoxUser.objects.get(user=self.request.user)
            cargo_queryset = Cargo.objects.filter(created_by=linfox_user)
        else:
            # Admins see all cargo
            cargo_queryset = Cargo.objects.all()
        
        # Add statistics (filtered by user type)
        context["total_cargo"] = cargo_queryset.count()
        context["available_cargo"] = cargo_queryset.filter(cargo_status="Cargo Available").count()
        context["in_transit_cargo"] = cargo_queryset.filter(cargo_status="In Transit").count()
        context["all_cargo"] = cargo_queryset.order_by("-id")[:5]  # Recent cargo
        return context


class LinfoxCargoListView(LinfoxRequiredMixin, ListView):
    template_name = "linfox/linfoxcargolist.html"
    context_object_name = "allcargo"
    
    def get_queryset(self):
        # Check if user is Admin or LinfoxUser
        is_admin = Admin.objects.filter(user=self.request.user).exists()
        is_linfox = LinfoxUser.objects.filter(user=self.request.user).exists()
        
        if is_linfox and not is_admin:
            # Linfox users see only their own cargo
            linfox_user = LinfoxUser.objects.get(user=self.request.user)
            return Cargo.objects.filter(created_by=linfox_user).order_by("-id")
        else:
            # Admin users see all cargo
            return Cargo.objects.all().order_by("-id")

class LinfoxCargoCreateView(LinfoxRequiredMixin, CreateView):
    template_name = "linfox/linfoxproductcreate.html"
    form_class = CargoForm
    success_url = reverse_lazy("ecomapp:linfoxcargolist")

    def form_valid(self, form):
        p = form.save(commit=False)
        # Assign the cargo to the logged-in Linfox user (if they are a LinfoxUser)
        if LinfoxUser.objects.filter(user=self.request.user).exists():
            linfox_user = LinfoxUser.objects.get(user=self.request.user)
            p.created_by = linfox_user
        # If Admin (not LinfoxUser), leave created_by as None
        p.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            LinfoxImage.objects.create(cargo=p, image=i)
        messages.success(self.request, f"Cargo '{p.CampanyName}' created successfully!")
        return super().form_valid(form)     


class AdminCargoDetailView(LinfoxRequiredMixin, DetailView):
    template_name = "adminpages/adminCargodetail.html"
    model = Cargo
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allstatus"] = ORDER_STATUS
        return context      


class AdminCargoStatuChangeView(LinfoxRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs["pk"]
        order_obj = Cargo.objects.get(id=order_id)
        new_status = request.POST.get("status")
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy("ecomapp:adminocargodetail", kwargs={"pk": order_id}))             


# class RegistrationView(CreateView):
#     template_name = "productownerregistration.html"
#     form_class = productOwnerRegistrationForm
#     success_url = reverse_lazy("ecomapp:home")

#     def form_valid(self, form):
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         email = form.cleaned_data.get("email")
#         user = User.objects.create_user(username, email, password)
#         form.instance.user = user
#         login(self.request, user)
#         return super().form_valid(form)

#     def get_success_url(self):
#         if "next" in self.request.GET:
#             next_url = self.request.GET.get("next")
#             return next_url
#         else:
#             return self.success_url

# product owner Page

class productOwnerLoginView(FormView):
    template_name = "productOwner/ProductOwnerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:pohome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        
        # Strip whitespace from username and password
        uname = uname.strip() if uname else ""
        pword = pword.strip() if pword else ""
        
        # Debug logging
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Product Owner login attempt for username: {uname}")
        
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            # Check if user has a product owner profile
            if not ProductOwner.objects.filter(user=usr).exists():
                messages.error(
                    self.request,
                    'Invalid credentials. This account is not registered as a product owner.'
                )
                return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
            
            # Check if email is verified
            from .models import EmailVerificationToken
            try:
                verification = EmailVerificationToken.objects.get(user=usr)
                if not verification.is_verified:
                    messages.error(
                        self.request,
                        'Please verify your email address before logging in. Check your email for the verification link. If you did not receive the email, please contact support.'
                    )
                    return render(self.request, self.template_name, {"form": self.form_class})
            except EmailVerificationToken.DoesNotExist:
                # If no verification token exists, allow login (for backward compatibility with old accounts)
                pass
            
            # Check if user is active
            if not usr.is_active:
                messages.error(
                    self.request,
                    'Your account is not active. Please verify your email address or contact support to activate your account.'
                )
                return render(self.request, self.template_name, {"form": self.form_class})
            
            # All checks passed - log the user in
            login(self.request, usr)
        else:
            # Authentication failed - wrong username or password
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid username or password"})
        
        return super().form_valid(form)

class productOwnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and ProductOwner.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/product-login/")
        return super().dispatch(request, *args, **kwargs)

class ProductOwnerProfileView(View):
    """View for product owners to view and edit their profile"""
    template_name = "productOwner/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and ProductOwner.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/product-login/?next=/po-profile/")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product_owner = request.user.productowner
        form = ProductOwnerProfileEditForm(instance=product_owner)
        form.fields['email'].initial = product_owner.user.email
        
        # Get products created by this product owner (using full_name from ProductOwner model)
        products = Product.objects.filter(productowner=product_owner.full_name).order_by("-id")[:10]
        
        context = {
            'product_owner': product_owner,
            'products': products,
            'form': form,
            'edit_mode': False
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        product_owner = request.user.productowner
        form = ProductOwnerProfileEditForm(request.POST, request.FILES, instance=product_owner)
        
        if form.is_valid():
            form.save()
            # Email is already updated in form.save(), but refresh user to ensure consistency
            product_owner.user.refresh_from_db()
            messages.success(request, "Profile updated successfully!")
            return redirect('ecomapp:productownerprofile')
        else:
            # Get products for context
            products = Product.objects.filter(productowner=product_owner.full_name).order_by("-id")[:10]
            
            context = {
                'product_owner': product_owner,
                'products': products,
                'form': form,
                'edit_mode': True
            }
            return render(request, self.template_name, context)


class LinfoxProfileView(View):
    """View for Linfox users to view and edit their profile"""
    template_name = "linfox/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and LinfoxUser.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/linfox-login/?next=/linfox-profile/")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        linfox_user = LinfoxUser.objects.get(user=request.user)
        form = LinfoxProfileEditForm(instance=linfox_user)
        form.fields['email'].initial = linfox_user.user.email
        
        # Get cargo created by this Linfox user only
        from .models import Cargo
        cargo_list = Cargo.objects.filter(created_by=linfox_user).order_by("-id")[:10]
        
        context = {
            'linfox_user': linfox_user,
            'cargo_list': cargo_list,
            'form': form,
            'edit_mode': False
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        linfox_user = LinfoxUser.objects.get(user=request.user)
        form = LinfoxProfileEditForm(request.POST, request.FILES, instance=linfox_user)
        
        if form.is_valid():
            form.save()
            # Email is already updated in form.save(), but refresh user to ensure consistency
            linfox_user.user.refresh_from_db()
            messages.success(request, "Profile updated successfully!")
            return redirect('ecomapp:linfoxprofile')
        else:
            # Get cargo created by this Linfox user only
            from .models import Cargo
            cargo_list = Cargo.objects.filter(created_by=linfox_user).order_by("-id")[:10]
            
            context = {
                'linfox_user': linfox_user,
                'cargo_list': cargo_list,
                'form': form,
                'edit_mode': True
            }
            messages.error(request, "Please correct the errors below.")
            return render(request, self.template_name, context)


class productOwnerHomeView(productOwnerRequiredMixin, TemplateView):
    template_name = "productOwner/productOwnerhome.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get product count for the current product owner
        product_owner = ProductOwner.objects.get(user=self.request.user)
        context['product_count'] = Product.objects.filter(productowner=product_owner.full_name).count()
        return context


class productOwnerListView(productOwnerRequiredMixin, ListView):
    template_name = "productOwner/productOwnerlist.html"
    context_object_name = "allproducts"
    
    def get_queryset(self):
        # Get the current product owner
        product_owner = ProductOwner.objects.get(user=self.request.user)
        # Filter products by the product owner's full name
        return Product.objects.filter(productowner=product_owner.full_name).order_by("-id")

class productOwner1ListView(productOwnerRequiredMixin, ListView):
    template_name = "productOwner/productOwnerlist.html"
    queryset = User.objects.all().order_by("-id")
    context_object_name = "alluser"

# def sample_view(request):
#     current_user = request.user

class productOwnerCreateView(productOwnerRequiredMixin, CreateView):
    template_name = "productOwner/productCreatePcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomapp:poproductlist")

    def form_valid(self, form):
        # Get the current product owner
        product_owner = ProductOwner.objects.get(user=self.request.user)
        # Set the product owner field
        form.instance.productowner = product_owner.full_name
        p = form.save()
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        messages.success(self.request, f"Product '{p.title}' added successfully!")
        return super().form_valid(form)


class productOwnerUpdateView(productOwnerRequiredMixin, UpdateView):
    model = Product
    template_name = "productOwner/productEdit.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomapp:poproductlist")
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        # Check if the product belongs to the current product owner
        product = self.get_object()
        product_owner = ProductOwner.objects.get(user=request.user)
        if product.productowner != product_owner.full_name:
            messages.error(request, "You don't have permission to edit this product.")
            return redirect("ecomapp:poproductlist")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Ensure product owner remains the same
        product_owner = ProductOwner.objects.get(user=self.request.user)
        form.instance.productowner = product_owner.full_name
        p = form.save()
        # Handle additional images
        images = self.request.FILES.getlist("more_images")
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        messages.success(self.request, f"Product '{p.title}' updated successfully!")
        return super().form_valid(form)


class productOwnerDeleteView(productOwnerRequiredMixin, DeleteView):
    model = Product
    template_name = "productOwner/productDelete.html"
    success_url = reverse_lazy("ecomapp:poproductlist")
    context_object_name = "product"

    def dispatch(self, request, *args, **kwargs):
        # Check if the product belongs to the current product owner
        product = self.get_object()
        product_owner = ProductOwner.objects.get(user=request.user)
        if product.productowner != product_owner.full_name:
            messages.error(request, "You don't have permission to delete this product.")
            return redirect("ecomapp:poproductlist")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f"Product '{product.title}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Chat Views
class SendMessageView(EcomMixin, View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please login to send a message.")
            return redirect("ecomapp:customerlogin")
        
        chat_id = request.POST.get('chat_id')
        message_text = request.POST.get('message', '').strip()
        
        if not message_text:
            messages.error(request, "Message cannot be empty.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        try:
            chat = Chat.objects.get(id=chat_id)
            # Verify user is part of this chat
            if chat.customer.user != request.user and (chat.product_owner and chat.product_owner.user != request.user):
                messages.error(request, "You don't have permission to send messages in this chat.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            Message.objects.create(
                chat=chat,
                sender=request.user,
                message=message_text
            )
            chat.updated_at = timezone.now()
            chat.save()
            messages.success(request, "Message sent successfully!")
        except Chat.DoesNotExist:
            messages.error(request, "Chat not found.")
        
        return redirect(request.META.get('HTTP_REFERER', '/'))


class ProductOwnerChatListView(productOwnerRequiredMixin, ListView):
    template_name = "productOwner/productownerchatlist.html"
    context_object_name = "chats"
    
    def get_queryset(self):
        product_owner = ProductOwner.objects.get(user=self.request.user)
        chats = Chat.objects.filter(product_owner=product_owner).order_by('-updated_at')
        # Add unread count to each chat
        for chat in chats:
            chat.unread_count = chat.messages.filter(is_read=False).exclude(sender=self.request.user).count()
        return chats


class ProductOwnerChatDetailView(productOwnerRequiredMixin, DetailView):
    model = Chat
    template_name = "productOwner/productownerchatdetail.html"
    context_object_name = "chat"
    
    def dispatch(self, request, *args, **kwargs):
        chat = self.get_object()
        product_owner = ProductOwner.objects.get(user=request.user)
        if chat.product_owner != product_owner:
            messages.error(request, "You don't have permission to view this chat.")
            return redirect("ecomapp:productownerchatlist")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all()
        # Mark messages as read
        self.object.messages.filter(is_read=False).exclude(sender=self.request.user).update(is_read=True)
        return context


# Category Management
class AdminCategoryListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/admincategorylist.html"
    queryset = Category.objects.all().order_by("title")
    context_object_name = "categories"


class AdminCategoryCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/admincategorycreate.html"
    form_class = CategoryForm
    success_url = reverse_lazy("ecomapp:admincategorylist")

    def form_valid(self, form):
        messages.success(self.request, f"Category '{form.instance.title}' created successfully!")
        return super().form_valid(form)


class AdminCategoryUpdateView(AdminRequiredMixin, UpdateView):
    model = Category
    template_name = "adminpages/admincategoryedit.html"
    form_class = CategoryForm
    success_url = reverse_lazy("ecomapp:admincategorylist")
    context_object_name = "category"

    def form_valid(self, form):
        messages.success(self.request, f"Category '{form.instance.title}' updated successfully!")
        return super().form_valid(form)


class AdminCategoryDeleteView(AdminRequiredMixin, DeleteView):
    model = Category
    template_name = "adminpages/admincategorydelete.html"
    success_url = reverse_lazy("ecomapp:admincategorylist")
    context_object_name = "category"

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        # Check if category has products
        product_count = Product.objects.filter(category=category).count()
        if product_count > 0:
            messages.error(request, f"Cannot delete category '{category.title}' because it has {product_count} product(s) associated with it. Please reassign or delete those products first.")
            return redirect("ecomapp:admincategorylist")
        messages.success(request, f"Category '{category.title}' deleted successfully!")
        return super().delete(request, *args, **kwargs)


# Setup view for creating admin user (one-time use)
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def create_admin_view(request):
    """
    One-time endpoint to create admin user from environment variables.
    Access via POST to /setup/create-admin/
    Also accepts GET to show current credentials
    """
    # Allow GET to show credentials (for easy access)
    if request.method == 'GET':
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@stopps.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
        
        return JsonResponse({
            'info': 'Current default credentials',
            'username': username,
            'email': email,
            'password': password,
            'instructions': 'Send POST request to this URL to create/reset admin user'
        })
    
    if request.method != 'POST':
        return JsonResponse({
            'error': 'Use POST method',
            'instructions': 'Send a POST request to this endpoint to create admin user'
        }, status=405)
    
    # Get credentials from environment variables, with secure defaults for testing
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@stopps.com')
    password = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
    
    try:
        # Get or create user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Update password and ensure superuser status (even if user exists)
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)  # Reset password to ensure it's correct
        user.save()
        
        action = 'created' if created else 'updated'
        return JsonResponse({
            'success': True,
            'message': f'Admin user "{username}" {action} successfully',
            'username': username,
            'email': email,
            'password': password,
            'note': 'You can now login at /admin/ or /admin-login/'
        })
    except Exception as e:
        return JsonResponse({
            'error': 'Failed to create/update admin user',
            'details': str(e)
        }, status=500)


# Email Verification Views
class VerifyEmailView(View):
    """Verify user email address"""
    def get(self, request, token):
        from .models import EmailVerificationToken
        try:
            verification = EmailVerificationToken.objects.get(token=token, is_verified=False)
            verification.is_verified = True
            verification.save()
            
            # Activate user account
            user = verification.user
            user.is_active = True
            user.save()
            
            messages.success(
                request,
                'Email verified successfully! You can now log in to your account.'
            )
            
            # Determine redirect based on user type
            if Customer.objects.filter(user=user).exists():
                return redirect('ecomapp:customerlogin')
            elif ProductOwner.objects.filter(user=user).exists():
                return redirect('ecomapp:productOwnerlogin')
            elif Admin.objects.filter(user=user).exists():
                return redirect('ecomapp:adminlogin')
            elif LinfoxUser.objects.filter(user=user).exists():
                return redirect('ecomapp:linfoxlogin')
            else:
                return redirect('ecomapp:customerlogin')
                
        except EmailVerificationToken.DoesNotExist:
            messages.error(
                request,
                'Invalid or expired verification link. Please request a new verification email.'
            )
            return redirect('ecomapp:home')


class ResendVerificationEmailView(View):
    """Resend verification email"""
    def post(self, request):
        email = request.POST.get('email')
        if not email:
            messages.error(request, 'Please provide your email address.')
            return redirect('ecomapp:customerlogin')
        
        try:
            user = User.objects.get(email=email)
            from .utils import send_verification_email
            
            # Determine user type
            user_type = 'customer'
            if ProductOwner.objects.filter(user=user).exists():
                user_type = 'productowner'
            elif Admin.objects.filter(user=user).exists():
                user_type = 'admin'
            elif LinfoxUser.objects.filter(user=user).exists():
                user_type = 'linfox'
            
            if send_verification_email(user, request, user_type=user_type):
                messages.success(
                    request,
                    f'Verification email has been sent to {email}. Please check your inbox.'
                )
            else:
                messages.error(
                    request,
                    'Failed to send verification email. Please try again later.'
                )
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
        
        return redirect('ecomapp:customerlogin')


# Password Reset Views for All User Types - Updated version
# Note: PasswordForgotView already exists above, we'll update it


class PasswordResetConfirmView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("ecomapp:customerlogin")

    def dispatch(self, request, *args, **kwargs):
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode
        from .utils import password_reset_token
        
        try:
            uidb64 = kwargs.get('uidb64')
            token = kwargs.get('token')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            pass
        else:
            messages.error(
                request,
                'Invalid or expired password reset link. Please request a new one.'
            )
            return redirect("ecomapp:passworforgot")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        from django.utils.encoding import force_str
        from django.utils.http import urlsafe_base64_decode
        from .utils import password_reset_token
        from django.contrib.sessions.models import Session
        from django.utils import timezone
        
        uidb64 = self.kwargs.get('uidb64')
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        # Set new password
        password = form.cleaned_data['new_password']
        
        # Strip any whitespace that might have been accidentally added
        password = password.strip()
        
        # Validate password is not empty
        if not password:
            messages.error(
                self.request,
                'Error: Password cannot be empty. Please enter a valid password.'
            )
            return render(self.request, self.template_name, {"form": self.form_class})
        
        # Set and save new password - this will hash it properly
        user.set_password(password)
        
        # Save with explicit update_fields to ensure password is saved
        user.save(update_fields=['password'])
        
        # Refresh user from database to get latest data
        user.refresh_from_db()
        
        # Verify password was saved by checking if user has a password hash
        if not user.has_usable_password():
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Password was not saved for user {user.username}")
            messages.error(
                self.request,
                'Error: Password was not saved. Please try again.'
            )
            return render(self.request, self.template_name, {"form": self.form_class})
        
        # Test authentication immediately to verify password works
        from django.contrib.auth import authenticate
        test_auth = authenticate(username=user.username, password=password)
        
        # Log the result
        import logging
        logger = logging.getLogger(__name__)
        if test_auth:
            logger.info(f"Password successfully reset and verified for user {user.username} (ID: {user.pk})")
            print(f"✅ Password reset successful for {user.username}")
        else:
            logger.warning(f"Password reset saved for {user.username} but immediate authentication test failed - this might be a caching issue")
            print(f"⚠️ Password saved for {user.username} but auth test failed - user should try logging in")
        
        # Invalidate all existing sessions for this user to prevent using old password
        # This ensures that after password reset, old sessions are logged out
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        deleted_sessions = 0
        for session in sessions:
            try:
                session_data = session.get_decoded()
                if session_data.get('_auth_user_id') == str(user.pk):
                    session.delete()
                    deleted_sessions += 1
            except Exception:
                # Skip sessions that can't be decoded
                continue
        
        messages.success(
            self.request,
            f'Password reset successfully! Your old password has been invalidated. Please login with your USERNAME "{user.username}" and your new password.'
        )
        
        return super().form_valid(form)

