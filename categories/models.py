from django.db import models


class ServiceCategory(models.Model):
    """
    A hireable job type: Plumbing, Electrical Work, Grocery Transport,
    House Cleaning, Pet Care, etc. Seeded via migration/fixture and
    managed from the admin.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True)
    description = models.TextField(blank=True)
    service_image=models.ImageField(upload_to='services/', blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, help_text="Icon name/key for the frontend")
    base_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Starting/callout price")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Service categories"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        return self.service_image.url if self.service_image else None
