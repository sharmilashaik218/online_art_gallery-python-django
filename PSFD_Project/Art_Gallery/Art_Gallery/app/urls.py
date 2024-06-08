from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm
urlpatterns=[
    path('',home,name='home'),
    path('category/<slug:val>',CategoryView.as_view(),name="category"),
    path('productdetails/<int:pk>',ProductDetails.as_view(),name="product-details"),
    path('contactus',contactus,name="contactus"),
    path('aboutus',aboutus,name="aboutus"),

    path('addtocart',add_to_cart,name="addtocart"),
    path('cart',show_cart,name="showcart"),
    path('pluscart/',plus_cart),
    path('minuscart/',minus_cart),
    path('removecart/',remove_cart),
    path('paymentdone/', payment_done, name='paymentdone'),
    path('checkout/',checkout.as_view(),name='checkout'),
    path('signup',CustomerRegister.as_view(),name="registration"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/',address, name='address'),
    path('updateaddress/<int:pk>', UpdateAddress.as_view(), name='updateaddress'),
    path('login',auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm),name='login'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="password_reset.html",form_class=MyPasswordResetForm),name="passwordreset"),
    path('password-change',auth_views.PasswordChangeView.as_view(template_name="password_change.html",form_class=MyPasswordChangeForm,success_url='/passwordchangedone'),name="passwordchange"),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name="passwordchangedone"),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password_reset/done',auth_views.PasswordChangeDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)