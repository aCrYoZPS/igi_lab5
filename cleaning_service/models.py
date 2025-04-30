from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import uuid

# --- Service Related Models ---


class ServiceType(models.Model):
    """Categorizes services (e.g., Residential, Commercial, Deep Clean)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    """Represents a specific cleaning service."""
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, related_name='services')
    name = models.CharField(max_length=200)
    description = models.TextField(help_text="Detailed description of what the service includes.")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    notes = models.TextField(blank=True, null=True, help_text="Additional notes for internal use or price list.")
    is_active = models.BooleanField(default=True, help_text="Is this service currently offered?")

    def __str__(self):
        return f"{self.name} ({self.service_type.name})"


# --- User and Staff Related Models ---


class Client(models.Model):
    """Represents a client."""
    class ClientType(models.TextChoices):
        PRIVATE = 'PRIVATE', 'Private Individual'
        COMPANY = 'COMPANY', 'Company'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile',
                                null=True, blank=True,
                                help_text="Link to Django User for login (optional for initial entry)")
    name = models.CharField(max_length=200, help_text="Customer name or Company name")
    contact_person = models.CharField(max_length=150, blank=True, null=True, help_text="Contact person if company")
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True, blank=True, null=True)  # Can be populated from User later
    client_type = models.CharField(max_length=10, choices=ClientType.choices, default=ClientType.PRIVATE)
    address = models.TextField(blank=True, null=True, help_text="Primary address (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """Represents a staff member."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='staff_profile', help_text="Link to Django User for login")
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    hire_date = models.DateField()
    role = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Cleaner, Manager, Receptionist")
    is_active = models.BooleanField(default=True)
    specializations = models.ManyToManyField(
        Service,
        through='StaffSpecialization',
        related_name='specialized_staff'
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class StaffSpecialization(models.Model):
    """Intermediate model linking Staff to the Services they specialize in."""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('staff', 'service')

    def __str__(self):
        return f"{self.staff} specializes in {self.service.name}"


# --- Order Related Models ---
class PromoCode(models.Model):
    """Represents promo codes or coupons."""
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'PERCENT', 'Percentage'
        FIXED = 'FIXED', 'Fixed Amount'

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices)
    value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount or percentage value")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(
        null=True, blank=True, help_text="Maximum number of times this code can be used overall")
    used_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.discount_type == self.DiscountType.PERCENTAGE:
            return f"{self.code} ({self.value}%)"
        else:
            return f"{self.code} (${self.value} Fixed)"


class Order(models.Model):
    """Represents a customer's order for one or more services."""
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Confirmation'
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class PaymentStatus(models.TextChoices):
        UNPAID = 'UNPAID', 'Unpaid'
        PAID = 'PAID', 'Paid'

    order_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                                  help_text="Unique identifier for the order")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='orders')
    address = models.TextField(help_text="Address where cleaning work will be performed")
    work_date = models.DateTimeField(help_text="Scheduled date and time for the cleaning work")
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                       help_text="Calculated total cost of the order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_orders', help_text="Staff member who entered the order")
    assigned_staff = models.ManyToManyField(Staff, related_name='assigned_orders',
                                            blank=True, help_text="Staff members assigned to this job")
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')

    def __str__(self):
        return f"Order {self.order_code} for {self.client.name}"

    def calculate_total(self):
        """Calculates the total amount based on order items."""
        total = sum(item.price_at_order * item.quantity for item in self.items.all())
        self.total_amount = total
        self.save(update_fields=['total_amount'])
        return total


class OrderItem(models.Model):
    """Links a specific Service to an Order, including quantity and price at the time."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2,
                                         help_text="Price of the service unit when the order was placed")

    class Meta:
        unique_together = ('order', 'service')

    def __str__(self):
        return f"{self.quantity} x {self.service.name} for Order {self.order.order_code}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.price_at_order:
            self.price_at_order = self.service.price
        super().save(*args, **kwargs)
