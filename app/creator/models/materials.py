from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking
from creator.models import Creator


class MaterialCategory(ActivityTracking):
    category_title = models.CharField(max_length=40, blank=True, null=True, default='')
    category_image = models.ImageField(upload_to="material_category", null=True,  blank=True, verbose_name=_("category image"))

    def __str__(self):
        return f"{self.category_title}"

    class Meta:
        verbose_name = "Material Category"
        verbose_name_plural = "Material Categories"
        ordering = ["-created_at"]

class Material(ActivityTracking):
    creator = models.ForeignKey("Creator", on_delete=models.CASCADE, related_name="material_creator")
    material_category = models.ForeignKey("MaterialCategory", on_delete=models.CASCADE, related_name="material_category")
    title = models.CharField(max_length=80, blank=True, null=True, default='')
    thumbnail_file = models.FileField(upload_to="materials", null=True,  blank=True, verbose_name=_("material thumbnail"))
    material_file = models.FileField(upload_to="materials", null=True,  blank=True, verbose_name=_("material file"))
    
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        ordering = ["-created_at"]


