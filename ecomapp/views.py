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
            cart_obj = Cart.objects.create(total=0)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
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
        # Get all available cargo options
        context['available_cargo'] = Cargo.objects.filter(cargo_status="Cargo Available")
        return context


class CheckoutView(EcomMixin, CreateView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("ecomapp:home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return redirect("/login/?next=/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
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
    success_url = reverse_lazy("ecomapp:pohome")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
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
    success_url = reverse_lazy("ecomapp:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
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
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

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


class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context


class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
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
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
            "/" + password_reset_token.make_token(user) + "/"
        send_mail(
            'Password Reset Link | Django STOPPS',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=True,
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
        user.set_password(password)
        user.save()
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
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            is_admin = Admin.objects.filter(user=usr).exists()
            is_linfox = LinfoxUser.objects.filter(user=usr).exists()
            
            if is_admin:
                # Super Admin can login and access admin dashboard
                login(self.request, usr)
                return redirect("ecomapp:adminhome")
            elif is_linfox:
                # LinfoxUser should use Linfox login page
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Linfox users should login from the Linfox login page. Please use /linfox-login/ instead."
                })
            else:
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Invalid credentials or you are not authorized to access the admin dashboard."
                })
        else:
            return render(self.request, self.template_name, {
                "form": self.form_class, 
                "error": "Invalid credentials"
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
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        messages.success(self.request, f"Product Owner '{form.instance.full_name}' created successfully!")
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
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        messages.success(self.request, f"Customer '{form.instance.full_name}' created successfully!")
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
        messages.success(self.request, "Cargo created successfully!")
        return super().form_valid(form)


class AdminCargoUpdateView(AdminRequiredMixin, UpdateView):
    model = Cargo
    template_name = "adminpages/admincargoedit.html"
    form_class = CargoForm
    success_url = reverse_lazy("ecomapp:linfoxcargolist")
    context_object_name = "cargo"

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
        usr = authenticate(username=uname, password=pword)
        if usr is not None:
            is_admin = Admin.objects.filter(user=usr).exists()
            is_linfox = LinfoxUser.objects.filter(user=usr).exists()
            
            if is_linfox:
                # LinfoxUser can only access Linfox dashboard
                login(self.request, usr)
                return redirect("ecomapp:linfoxhome")
            elif is_admin:
                # Admin users should use admin login page
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Admin users should login from the admin login page. Please use /admin-login/ instead."
                })
            else:
                return render(self.request, self.template_name, {
                    "form": self.form_class, 
                    "error": "Invalid credentials or you are not authorized"
                })
        else:
            return render(self.request, self.template_name, {
                "form": self.form_class, 
                "error": "Invalid credentials"
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
        # Add statistics
        context["total_cargo"] = Cargo.objects.count()
        context["available_cargo"] = Cargo.objects.filter(cargo_status="Cargo Available").count()
        context["in_transit_cargo"] = Cargo.objects.filter(cargo_status="In Transit").count()
        context["all_cargo"] = Cargo.objects.all().order_by("-id")[:5]  # Recent cargo
        return context


class LinfoxCargoListView(LinfoxRequiredMixin, ListView):
    template_name = "linfox/linfoxcargolist.html"
    queryset = Cargo.objects.all().order_by("-id")
    context_object_name = "allcargo"

class LinfoxCargoCreateView(LinfoxRequiredMixin, CreateView):
    template_name = "linfox/linfoxproductcreate.html"
    form_class = CargoForm
    success_url = reverse_lazy("ecomapp:linfoxcargolist")

    def form_valid(self, form):
        p = form.save()
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
        usr = authenticate(username=uname, password=pword)
        if usr is not None and ProductOwner.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        return super().form_valid(form)

class productOwnerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and ProductOwner.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/product-login/")
        return super().dispatch(request, *args, **kwargs)

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

