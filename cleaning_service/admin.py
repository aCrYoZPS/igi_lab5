from django.contrib import admin
from .models import (ServiceType, Service, Client,
                     Staff, StaffSpecialization,
                     PromoCode, Order, OrderItem,
                     FAQ, Vacancy, Review, About,
                     PrivacyPolicy)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price_at_order',)


class StaffSpecializationInline(admin.TabularInline):
    model = StaffSpecialization
    extra = 1


@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'price', 'is_active')
    list_filter = ('service_type', 'is_active')
    search_fields = ('name', 'description', 'notes')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_type', 'contact_number', 'email', 'user')
    list_filter = ('client_type',)
    search_fields = ('name', 'contact_person', 'contact_number', 'email')
    raw_id_fields = ('user',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'contact_number', 'hire_date', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'contact_number')
    inlines = [StaffSpecializationInline]
    raw_id_fields = ('user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'client', 'work_date', 'status', 'payment_status', 'total_amount', 'created_by')
    list_filter = ('status', 'payment_status', 'work_date', 'client', 'created_by')
    search_fields = ('order_code', 'client__name', 'address')
    readonly_fields = ('order_code', 'created_at', 'updated_at', 'total_amount')
    raw_id_fields = ('client', 'created_by', 'promo_code')
    filter_horizontal = ('assigned_staff',)
    inlines = [OrderItemInline]
    date_hierarchy = 'work_date'

    actions = ['recalculate_totals', 'mark_as_paid']

    def recalculate_totals(self, request, queryset):
        for order in queryset:
            order.calculate_total()
            order.save(update_fields=['total_amount'])
        self.message_user(request, f"Recalculated totals for {queryset.count()} orders.")
    recalculate_totals.short_description = "Recalculate selected order totals"

    def mark_as_paid(self, request, queryset):
        updated_count = queryset.update(payment_status=Order.PaymentStatus.PAID)
        self.message_user(request, f"Marked {updated_count} orders as paid.")
    mark_as_paid.short_description = "Mark selected orders as Paid"


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'value', 'valid_from', 'valid_to', 'is_active', 'used_count', 'max_uses')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    pass


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    pass


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    pass
