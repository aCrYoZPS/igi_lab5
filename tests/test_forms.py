from django.test import TestCase
from django.forms import formset_factory
from django.utils import timezone
from cleaning_service.models import PromoCode, Service, ServiceType
from cleaning_service.forms import OrderForm, OrderItemFormSet
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderFormTest(TestCase):
    def setUp(self):
        self.service_type = ServiceType.objects.create(name="Residential")
        self.service = Service.objects.create(
            service_type=self.service_type,
            name="Basic Cleaning",
            price=100.00
        )
        self.active_promo = PromoCode.objects.create(
            code="VALID20",
            discount_type=PromoCode.DiscountType.PERCENTAGE,
            value=20,
            valid_from=timezone.now() - timezone.timedelta(days=1),
            valid_to=timezone.now() + timezone.timedelta(days=1),
            is_active=True
        )
        self.expired_promo = PromoCode.objects.create(
            code="EXPIRED",
            discount_type=PromoCode.DiscountType.FIXED,
            value=50,
            valid_from=timezone.now() - timezone.timedelta(days=2),
            valid_to=timezone.now() - timezone.timedelta(days=1),
            is_active=True
        )

    def test_form_fields(self):

        form = OrderForm()
        self.assertIn("datetime-local", str(form["work_date"].as_widget()))
        self.assertIn('rows="3"', str(form["address"].as_widget()))

    def test_valid_promo_code_selection(self):
        form = OrderForm(data={
            "address": "123 Main St",
            "work_date": timezone.now(),
            "promo_code": self.active_promo.id
        })
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        form = OrderForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("address", form.errors)
        self.assertIn("work_date", form.errors)


class OrderItemFormSetTest(TestCase):
    def setUp(self):
        self.service_type = ServiceType.objects.create(name="Commercial")
        self.service1 = Service.objects.create(
            service_type=self.service_type,
            name="Office Cleaning",
            price=200.00
        )
        self.service2 = Service.objects.create(
            service_type=self.service_type,
            name="Window Cleaning",
            price=150.00
        )

    def test_min_items_validation(self):
        FormSet = formset_factory(OrderItemFormSet.form, formset=OrderItemFormSet)
        formset = FormSet(data={
            "items-TOTAL_FORMS": "0",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "1",
            "items-MAX_NUM_FORMS": "3",
        })
        self.assertFalse(formset.is_valid())
        self.assertWarnsMessage
        self.assertIn("at least", formset.non_form_errors()[0])

    def test_mquantity_validation(self):
        FormSet = formset_factory(OrderItemFormSet.form, formset=OrderItemFormSet)
        formset = FormSet(data={
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-0-service": self.service1.id,
            "items-0-quantity": 0,
        })
        self.assertFalse(formset.is_valid())
        self.assertIn("quantity", formset.forms[0].errors)
        self.assertIn("Ensure this value is greater than or equal to 1",
                      formset.forms[0].errors["quantity"][0])

    def test_valid_formset_submission(self):
        FormSet = formset_factory(OrderItemFormSet.form, formset=OrderItemFormSet)
        formset = FormSet(data={
            "items-TOTAL_FORMS": "2",
            "items-INITIAL_FORMS": "0",
            "items-0-service": self.service1.id,
            "items-0-quantity": 2,
            "items-1-service": self.service2.id,
            "items-1-quantity": 1,
        })
        self.assertTrue(formset.is_valid())

    def test_duplicate_service_validation(self):
        """Test prevention of duplicate services in order items"""
        FormSet = formset_factory(OrderItemFormSet.form, formset=OrderItemFormSet)
        formset = FormSet(data={
            "items-TOTAL_FORMS": "2",
            "items-INITIAL_FORMS": "0",
            "items-0-service": self.service1.id,
            "items-0-quantity": 1,
            "items-1-service": self.service1.id,
            "items-1-quantity": 1,
        })
        self.assertFalse(formset.is_valid())
        self.assertIn("duplicate", formset.forms[1].errors["__all__"][0])
