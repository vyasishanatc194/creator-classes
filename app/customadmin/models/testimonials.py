from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking


class Testimonial(ActivityTracking):
    image = models.ImageField(upload_to="testimonials", null=True,  blank=True, verbose_name=_("testimonial image"))
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    email = models.EmailField(blank=True, null=True)
    testimonial_text = models.TextField(max_length=500, blank=True, null=True, default='')
    rating = models.FloatField(blank=True, null=True, default=1)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ["-created_at"]
