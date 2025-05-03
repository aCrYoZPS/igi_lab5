"""
URL configuration for cleaning_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("admin/", admin.site.urls),
    path("faq/", views.faq, name="faq"),
    path("jobs/", views.vacancies, name="vacancies"),
    path("about/", views.about, name="about"),
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("cat_fact/", views.CatFactView.as_view(), name="cat_fact"),
    path("promo/", views.PromoCodeView.as_view(), name="promo_codes"),
    path("service_types/", views.ServiceTypeView.as_view(), name="service_types"),
    path("services/", views.ServiceView.as_view(), name="services"),
    path("orders/", views.OrderView.as_view(), name="orders"),
    path('orders/create/', views.AddOrderView.as_view(), name='order_create'),
    path("", include("users.urls")),
    path("", include("blog.urls")),
    path("", include("reviews.urls")),
    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
