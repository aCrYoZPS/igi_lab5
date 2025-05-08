from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from cleaning_service.models import *
from blog.models import Article
from decimal import Decimal
import uuid

User = get_user_model()

# Service models


class ServiceTypeModelTest(TestCase):
    def test_create_service_type(self):
        st = ServiceType.objects.create(
            name="Residential Cleaning",
            description="Home cleaning services"
        )
        self.assertEqual(st.name, "Residential Cleaning")
        self.assertEqual(str(st), "Residential Cleaning")


class ServiceModelTest(TestCase):
    def setUp(self):
        self.service_type = ServiceType.objects.create(name="Commercial")

    def test_service_creation(self):
        service = Service.objects.create(
            service_type=self.service_type,
            name="Office Deep Clean",
            description="Thorough office cleaning",
            price=299.99
        )
        self.assertEqual(service.price, 299.99)
        self.assertTrue(service.is_active)
        self.assertEqual(str(service), "Office Deep Clean (Commercial)")

    def test_price_validation(self):
        with self.assertRaises(ValidationError):
            Service.objects.create(
                service_type=self.service_type,
                name="Invalid Service",
                price=-100
            ).full_clean()


class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="client1", password="testpass123"
        )

    def test_client_creation(self):
        client = Client.objects.create(
            user=self.user,
            name="John Doe",
            contact_number="+375291234567",
            client_type=Client.ClientType.PRIVATE
        )
        self.assertEqual(client.client_type, "PRIVATE")
        self.assertEqual(str(client), "John Doe")

    def test_company_client(self):
        client = Client.objects.create(
            name="CleanCo Ltd",
            contact_person="Jane Smith",
            contact_number="+375441234567",
            client_type=Client.ClientType.COMPANY
        )
        self.assertEqual(client.contact_person, "Jane Smith")


class StaffModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="staff1",
            first_name="Alice",
            last_name="Smith",
            password="testpass123"
        )
        self.service_type = ServiceType.objects.create(name="Residential")
        self.service = Service.objects.create(
            service_type=self.service_type,
            name="Basic Clean",
            price=100
        )

    def test_staff_creation(self):
        staff = Staff.objects.create(
            user=self.user,
            hire_date="2023-01-01"
        )
        staff.specializations.add(self.service)
        self.assertEqual(str(staff), "Alice Smith")
        self.assertEqual(staff.specializations.count(), 1)


class PromoCodeModelTest(TestCase):
    def test_promo_code_creation(self):
        promo = PromoCode.objects.create(
            code="SPRING20",
            discount_type=PromoCode.DiscountType.PERCENTAGE,
            value=20,
            valid_from=timezone.now(),
            valid_to=timezone.now() + timedelta(days=7)
        )
        self.assertEqual(promo.used_count, 0)
        self.assertTrue(promo.is_active)
        self.assertIn("20%", str(promo))


class OrderModelTest(TestCase):
    def setUp(self):
        self.client_user = Client.objects.create(
            name="Test Client",
            contact_number="+375291234567"
        )
        self.service_type = ServiceType.objects.create(name="Residential")
        self.service = Service.objects.create(
            service_type=self.service_type,
            name="Basic Clean",
            price=100
        )
        self.staff_user = Staff.objects.create(
            user=User.objects.create_user(username="staff1"),
            hire_date="2023-01-01"
        )

    def test_order_creation(self):
        order = Order.objects.create(
            client=self.client_user,
            address="Test Address",
            work_date=timezone.now(),
            created_by=self.staff_user
        )
        self.assertEqual(order.status, Order.OrderStatus.PENDING)
        self.assertIsInstance(order.order_code, uuid.UUID)

    def test_total_calculation(self):
        order = Order.objects.create(
            client=self.client_user,
            address="Test Address",
            work_date=timezone.now()
        )
        OrderItem.objects.create(
            order=order,
            service=self.service,
            quantity=2,
            price_at_order=self.service.price
        )
        order.save_calculate_total()
        self.assertEqual(order.total_amount, Decimal('200'))

    def test_promo_code_discount(self):
        promo = PromoCode.objects.create(
            code="FIXED50",
            discount_type=PromoCode.DiscountType.FIXED,
            value=50,
            valid_from=timezone.now(),
            valid_to=timezone.now() + timedelta(days=1)
        )
        order = Order.objects.create(
            client=self.client_user,
            address="Test Address",
            work_date=timezone.now(),
            promo_code=promo
        )
        OrderItem.objects.create(
            order=order,
            service=self.service,
            quantity=1,
            price_at_order=self.service.price
        )
        order.save_calculate_total()
        self.assertEqual(order.total_amount, Decimal('50'))


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(name="Test", contact_number="+375291234567")
        self.service = Service.objects.create(
            service_type=ServiceType.objects.create(name="Test"),
            name="Test Service",
            price=100
        )
        self.order = Order.objects.create(
            client=self.client,
            address="Test",
            work_date=timezone.now()
        )

    def test_order_item_creation(self):
        item = OrderItem.objects.create(
            order=self.order,
            service=self.service,
            quantity=3
        )
        self.assertEqual(item.price_at_order, Decimal('100'))
        self.assertEqual(item.quantity, 3)


class SupportModelsTest(TestCase):
    def test_faq_creation(self):
        faq = FAQ.objects.create(
            question="How does it work?",
            answer="Very simple!"
        )
        self.assertIsInstance(faq.answer_date, datetime)

    def test_vacancy_creation(self):
        st = ServiceType.objects.create(name="Commercial")
        vacancy = Vacancy.objects.create(
            job_title="Cleaner",
            job_description="Need experienced cleaner",
            job_type=st
        )
        self.assertEqual(vacancy.job_type, st)

    def test_about_creation(self):
        about = About.objects.create(
            history="Founded in 2020",
            contact_info="Call us!"
        )
        self.assertEqual(str(about), "About Info")

    def test_privacy_policy(self):
        pp = PrivacyPolicy.objects.create(
            policy_content="We respect your privacy"
        )
        self.assertEqual(str(pp), "Privacy policy")

# Blog models


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testauthor',
            email='author@test.com',
            password='testpass123'
        )
        self.article_data = {
            'title': 'Test Article Title',
            'content': 'This is the article content',
            'author': self.user,
        }

    def test_article_creation(self):
        """Test basic article creation with required fields"""
        article = Article.objects.create(**self.article_data)

        self.assertEqual(article.title, 'Test Article Title')
        self.assertEqual(article.content, 'This is the article content')
        self.assertEqual(article.author, self.user)
        self.assertEqual(article.summary, '')
        self.assertIsNone(article.img)
        self.assertIsInstance(article.publication_date, timezone.datetime)

    def test_str_representation(self):
        """Test the string representation of the article"""
        article = Article.objects.create(**self.article_data)
        expected_str = (
            f"{article.title} by {self.user}. "
            f"Published on {article.publication_date.strftime('%d/%m/%Y %H:%M:%S')}"
        )
        self.assertEqual(str(article), expected_str)

    def test_title_max_length(self):
        """Test title field maximum length constraint"""
        article = Article.objects.create(
            title='A' * 256,
            content='Content',
            author=self.user,
            summary="sum"
        )
        article.full_clean()

        with self.assertRaises(ValidationError):
            article.title = 'A' * 257
            article.full_clean()

    def test_summary_field(self):
        """Test summary field behavior"""
        article = Article.objects.create(**self.article_data)
        self.assertEqual(article.summary, '')

        article.summary = 'Short summary'
        article.save()
        self.assertEqual(article.summary, 'Short summary')

        with self.assertRaises(ValidationError):
            article.summary = 'S' * 1025
            article.full_clean()

    def test_publication_date_auto_add(self):
        """Test automatic publication date setting"""
        before_creation = timezone.now()
        article = Article.objects.create(**self.article_data)
        after_creation = timezone.now()

        self.assertLessEqual(before_creation, article.publication_date)
        self.assertGreaterEqual(after_creation, article.publication_date)

    def test_author_relationship(self):
        """Test author foreign key relationship"""
        article = Article.objects.create(**self.article_data)

        self.assertEqual(article.author, self.user)
        self.assertIn(article, self.user.article_set.all())
        self.user.delete()
        with self.assertRaises(Article.DoesNotExist):
            Article.objects.get(pk=article.pk)

    def test_image_field(self):
        article = Article.objects.create(**self.article_data)
        self.assertIsNone(article.img)

        article.img = 'https://example.com/image.jpg'
        article.save()
        self.assertEqual(article.img, 'https://example.com/image.jpg')
