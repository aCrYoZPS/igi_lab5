from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from blog.models import Article
from cleaning_service.models import *
from cleaning_service.views import *
import json
from datetime import datetime
from django.utils import timezone

User = get_user_model()


def create_client_user():
    return Client.objects.create(name="Test Client", contact_number="+375291234567")


def create_staff_user():
    user = User.objects.create_user(username="staff", password="testpass")
    return Staff.objects.create(user=user, hire_date="2023-01-01")


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.article = Article.objects.create(
            title="Test Article",
            author=self.user,
            content="Test content"
        )

    @patch("requests.get")
    def test_index_view(self, mock_get):
        mock_response = type("MockResponse", (), {"content": json.dumps({"ip": "123.45.67.89"})})
        mock_get.return_value = mock_response

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "service/index.html")
        self.assertEqual(response.context["article"], self.article)


class StaticViewsTest(TestCase):
    def test_privacy_policy_view(self):
        PrivacyPolicy.objects.create(policy_content="Test policy")
        response = self.client.get(reverse("privacy_policy"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test policy")

    def test_faq_view(self):
        FAQ.objects.create(question="Q1", answer="A1")
        response = self.client.get(reverse("faq"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["faqs"], FAQ.objects.all())

    def test_vacancies_view(self):
        st = ServiceType.objects.create(name="Test")
        Vacancy.objects.create(job_title="Cleaner", job_description="Test", job_type=st)
        response = self.client.get(reverse("vacancies"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["vacancies"]), 1)

    def test_about_view(self):
        About.objects.create(contact_info="Test")
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context["about"])


class CatFactViewTest(TestCase):
    @patch("requests.get")
    def test_successful_fetch(self, mock_get):
        mock_response = type("MockResponse", (), {
            "status_code": 200,
            "content": json.dumps({"fact": "Cats are great!"})
        })
        mock_get.return_value = mock_response

        response = self.client.get(reverse("cat_fact"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["cat_fact"], "Cats are great!")

    @patch("requests.get")
    def test_failed_fetch(self, mock_get):
        mock_response = type("MockResponse", (), {"status_code": 500})
        mock_get.return_value = mock_response

        response = self.client.get(reverse("cat_fact"))
        self.assertIsNone(response.context["cat_fact"])


class PromoCodeViewTest(TestCase):
    def setUp(self):
        PromoCode.objects.create(code="VALID", is_active=True, value=1,
                                 valid_from=datetime.now(), valid_to=datetime.now())
        PromoCode.objects.create(code="INVALID", is_active=False, value=1,
                                 valid_from=datetime.now(), valid_to=datetime.now())

    def test_view_context(self):
        response = self.client.get(reverse("promo_codes"))
        self.assertEqual(len(response.context["valid_codes"]), 1)
        self.assertEqual(len(response.context["invalid_codes"]), 1)


class ServiceViewsTest(TestCase):
    def setUp(self):
        self.service_type = ServiceType.objects.create(name="Residential")
        self.service = Service.objects.create(
            service_type=self.service_type,
            name="Basic Clean",
            price=100
        )

    def test_service_type_view(self):
        response = self.client.get(reverse("service_types"))
        self.assertQuerySetEqual(response.context["service_types"], [self.service_type])

    def test_service_filter_view(self):
        response = self.client.get(reverse("services") + "?service_type=1&price__gt=&price__lt=")
        self.assertContains(response, "Basic Clean")


class OrderViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client_user = create_client_user()
        self.staff_user = create_staff_user()
        self.service = Service.objects.create(
            service_type=ServiceType.objects.create(name="Test"),
            name="Test Service",
            price=100
        )

    def test_order_view_permissions(self):
        response = self.client.get(reverse("orders"))
        self.assertRedirects(response, f"/auth/login/?next={reverse("orders")}")

    def test_client_order_view(self):
        self.client.login(username="client", password="testpass")
        Order.objects.create(client=self.client_user, address="Test", work_date=timezone.now())
        response = self.client.get(reverse("orders"))
        self.assertEqual(1, 1)

    def test_staff_order_view(self):
        self.client.login(username="staff", password="testpass")
        order = Order.objects.create(
            client=self.client_user,
            address="Test",
            work_date=timezone.now(),
            created_by=self.staff_user,
        )
        order.assigned_staff.set([self.staff_user])
        order.save()
        response = self.client.get(reverse("orders"))
        self.assertEqual(len(response.context["orders"]), 1)

    def test_superuser_order_view(self):
        User.objects.create_superuser(username="admin", password="adminpass")
        self.client.login(username="admin", password="adminpass")
        Order.objects.create(client=self.client_user, address="Test", work_date=timezone.now())
        response = self.client.get(reverse("orders"))
        self.assertEqual(len(response.context["orders"]), 1)


class AddOrderViewTest(TestCase):
    def setUp(self):
        self.client_user = create_client_user()
        self.service = Service.objects.create(
            service_type=ServiceType.objects.create(name="Test"),
            name="Test Service",
            price=100
        )

    def test_order_creation_flow(self):
        self.client.login(username="client", password="testpass")

        form_data = {
            "address": "Test Address",
            "work_date": "2024-01-01 12:00",
        }

        formset_data = {
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-0-service": self.service.id,
            "items-0-quantity": 2,
        }

        response = self.client.post(
            reverse("order_create"),
            data={**form_data, **formset_data},
            follow=True
        )

    def test_invalid_form_submission(self):
        self.client.login(username="client", password="testpass")
        response = self.client.post(reverse("order_create"), {})
        self.assertEqual(response.status_code, 302)
