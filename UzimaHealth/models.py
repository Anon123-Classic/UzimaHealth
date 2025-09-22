from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.auth.models import User
import uuid

class Bookings(models.Model):
    TEST_CHOICES = [
        ("blood-test", "Blood Test"),
        ("xray", "X-Ray"),
        ("mri", "MRI Scan"),
        ("ct-scan", "CT Scan"),
        ("covid-test", "COVID-19 Test"),
        ("general-checkup", "General Checkup"),
    ]

    HOSPITAL_CHOICES = [
        ("kenyatta", "Kenyatta National Hospital"),
        ("nairobi-hospital", "The Nairobi Hospital"),
        ("aga-khan", "Aga Khan University Hospital"),
        ("moi-teaching", "Moi Teaching & Referral Hospital"),
        ("coast-general", "Coast General Teaching & Referral Hospital"),
        ("other", "Other"),
    ]

    # 🔑 Allow null & blank so migrations won't fail on existing data
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True
    )

    patient_name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(120)])
    contact_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r"^07\d{8}$", "Enter a valid phone number e.g., 07XXXXXXXX")]
    )
    test_type = models.CharField(max_length=50, choices=TEST_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    hospital_name = models.CharField(max_length=100, choices=HOSPITAL_CHOICES)
    # New field for reference code
    booking_ref = models.CharField(max_length=20, editable=False, )  # Temporary default

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            # Example: UZIMA-20250922-AB12
            self.booking_ref = "UZIMA-" + uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["patient_name", "test_type", "date", "time"],
                name="unique_booking_per_patient"
            )
        ]

    def __str__(self):
        return f"{self.patient_name} - {self.get_test_type_display()} on {self.date} at {self.time}"
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
