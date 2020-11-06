# -*- coding: utf-8 -*-

from django import forms

from ..models import Testimonial


# -----------------------------------------------------------------------------
# Testimonials
# -----------------------------------------------------------------------------

class TestimonialCreationForm(forms.ModelForm):
    """Custom TestimonialCreationForm"""

    class Meta():
        model = Testimonial
        fields = [
            "image",
            "name",
            "email",
            "testimonial_text",
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        print(*args)

    def clean(self):
        cleaned_data = super(TestimonialCreationForm, self).clean()
        rating = cleaned_data.get("rating")

        if float(rating) < 0.0 or float(rating) > 5.0 :
            raise forms.ValidationError(
                "Rating must be grater then and equal to 0 and less than and equal to 5."
            )


    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class TestimonialChangeForm(forms.ModelForm):
    """Custom form to change Testimonials"""

    class Meta():
        model = Testimonial

        fields = [
            "image",
            "name",
            "email",
            "testimonial_text",
            "rating",
        ]

    def clean(self):
        cleaned_data = super(TestimonialChangeForm, self).clean()
        rating = cleaned_data.get("rating")

        if float(rating) < 0.0 or float(rating) > 10.0 :
            raise forms.ValidationError(
                "Rating must be grater then and equal to 0 and less than and equal to 10."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance