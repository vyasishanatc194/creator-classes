from django.db import models
from creator_class.models import ActivityTracking

class CountryField(ActivityTracking):
    country_name = models.CharField(max_length=100, blank=True, null=True)
    country_flag = models.ImageField(upload_to='country/', null=True, blank=True)

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name = "CountryField"
        verbose_name_plural = "CountryFields"
        ordering = ["country_name"]

    def clean(self):
        self.country_name=self.country_name.capitalize()


