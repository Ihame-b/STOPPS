from django.urls import path
from .views import *


app_name = "ecomapp"
urlpatterns = [

    # Client side pages
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact-us/", ContactView.as_view(), name="contact"),
    path("all-products/", AllProductsView.as_view(), name="allproducts"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="productdetail"),

    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("update-cargo/<int:cp_id>/", UpdateCargoView.as_view(), name="updatecargo"),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),

    path("khalti-request/", KhaltiRequestView.as_view(), name="khaltirequest"),
    path("khalti-verify/", KhaltiVerifyView.as_view(), name="khaltiverify"),

    path("esewa-request/", EsewaRequestView.as_view(), name="esewarequest"),
    path("esewa-verify/", EsewaVerifyView.as_view(), name="esewaverify"),

    path("register/",
         CustomerRegistrationView.as_view(), name="customerregistration"),

    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"),
    path("login/", CustomerLoginView.as_view(), name="customerlogin"),

    path("profile/", CustomerProfileView.as_view(), name="customerprofile"),
    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),

    path("search/", SearchView.as_view(), name="search"),

    path("forgot-password/", PasswordForgotView.as_view(), name="passworforgot"),
    path("password-reset/<email>/<token>/",
         PasswordResetView.as_view(), name="passwordreset"),
    
    # Admin Side pages

    path("admin-login/", AdminLoginView.as_view(), name="adminlogin"),

    path("admin-home/", AdminHomeView.as_view(), name="adminhome"),

    path("admin-order/<int:pk>/", AdminOrderDetailView.as_view(),
         name="adminorderdetail"),

    path("admin-all-orders/", AdminOrderListView.as_view(), name="adminorderlist"),

    path("admin-order-<int:pk>-change/",
         AdminOrderStatuChangeView.as_view(), name="adminorderstatuschange"),

    path("admin-product/list/", AdminProductListView.as_view(),
         name="adminproductlist"),

    path("admin-product/add/", AdminProductCreateView.as_view(),
         name="adminproductcreate"),

    path("admin-product/edit/<int:pk>/", AdminProductUpdateView.as_view(),
         name="adminproductedit"),

    path("admin-product/delete/<int:pk>/", AdminProductDeleteView.as_view(),
         name="adminproductdelete"),

    # Category Management
    path("admin-category/list/", AdminCategoryListView.as_view(),
         name="admincategorylist"),

    path("admin-category/add/", AdminCategoryCreateView.as_view(),
         name="admincategorycreate"),

    path("admin-category/edit/<int:pk>/", AdminCategoryUpdateView.as_view(),
         name="admincategoryedit"),

    path("admin-category/delete/<int:pk>/", AdminCategoryDeleteView.as_view(),
         name="admincategorydelete"),

    # Product Owner Management
    path("admin-productowner/list/", AdminProductOwnerListView.as_view(),
         name="adminproductownerlist"),

    path("admin-productowner/add/", AdminProductOwnerCreateView.as_view(),
         name="adminproductownercreate"),

    path("admin-productowner/edit/<int:pk>/", AdminProductOwnerUpdateView.as_view(),
         name="adminproductowneredit"),

    path("admin-productowner/delete/<int:pk>/", AdminProductOwnerDeleteView.as_view(),
         name="adminproductownerdelete"),

    # Customer Management
    path("admin-customer/list/", AdminCustomerListView.as_view(),
         name="admincustomerlist"),

    path("admin-customer/add/", AdminCustomerCreateView.as_view(),
         name="admincustomercreate"),

    path("admin-customer/edit/<int:pk>/", AdminCustomerUpdateView.as_view(),
         name="admincustomeredit"),

    path("admin-customer/delete/<int:pk>/", AdminCustomerDeleteView.as_view(),
         name="admincustomerdelete"),

    # Cargo/Transport Management
    path("admin-cargo/add/", AdminCargoCreateView.as_view(),
         name="admincargocreate"),

    path("admin-cargo/edit/<int:pk>/", AdminCargoUpdateView.as_view(),
         name="admincargoedit"),

    path("admin-cargo/delete/<int:pk>/", AdminCargoDeleteView.as_view(),
         name="admincargodelete"),

    # Order Management
    path("admin-order/edit/<int:pk>/", AdminOrderUpdateView.as_view(),
         name="adminorderedit"),

    path("admin-order/delete/<int:pk>/", AdminOrderDeleteView.as_view(),
         name="adminorderdelete"),

    #Linfox
#     path("linfox-login/", LinfoxLoginView.as_view(), name="linfoxlogin"),
    path("linfox-home/", LinfoxHomeView.as_view(), name="linfoxhome"),
    path("linfox-cargo/list/", LinfoxCargoListView.as_view(), name="linfoxcargolist"),
    path("linfox-cargo/add/",  LinfoxCargoCreateView.as_view(), name="linfoxproductcreate"),

#     path("admin-cargo/<int:pk>/", AdminCargoDetailView.as_view(), name="adminocargodetail"),
#     path("admin-cargo-<int:pk>-change/", AdminCargoStatuChangeView.as_view(), name="admincargostatuschange"),
    #


# Product Owner
    path("product-login/", productOwnerLoginView.as_view(), name="productOwnerlogin"),
    path("po-home/", productOwnerHomeView.as_view(), name="pohome"),
    path("po-pro/list/", productOwnerListView.as_view(), name="poproductlist"),
    path("po-pro/add/",  productOwnerCreateView.as_view(), name="poproductcreate"),
    path("po-pro/edit/<int:pk>/", productOwnerUpdateView.as_view(), name="poproductedit"),
    path("po-pro/delete/<int:pk>/", productOwnerDeleteView.as_view(), name="poproductdelete"),

    path("poregister/", ProductOwnerRegistrationView.as_view(), name="poregistration"),

    # Chat
    path("send-message/", SendMessageView.as_view(), name="sendmessage"),
    path("po-chats/", ProductOwnerChatListView.as_view(), name="productownerchatlist"),
    path("po-chat/<int:pk>/", ProductOwnerChatDetailView.as_view(), name="productownerchatdetail"),

    # Setup endpoint (one-time admin creation)
    path("setup/create-admin/", create_admin_view, name="create_admin"),

]
