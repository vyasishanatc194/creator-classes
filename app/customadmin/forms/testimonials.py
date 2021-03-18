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
            "name",
            "email",
            "image",
            "testimonial_text",
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TestimonialCreationForm, self).clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        image = cleaned_data.get("image")
        testimonial_text = cleaned_data.get("testimonial_text")
        rating = cleaned_data.get("rating")

        if not name :
            raise forms.ValidationError(
                "Please add name."
            )
        if not email :
            raise forms.ValidationError(
                "Please add email."
            )
        if not image :
            raise forms.ValidationError(
                "Please add testimonial image."
            )
        if not testimonial_text :
            raise forms.ValidationError(
                "Please add testimonial text."
            )
        if float(rating) < 0.0 or float(rating) > 5.0 :
            raise forms.ValidationError(
                "Rating must be grater than and equal to 0 and less than and equal to 5."
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
            "name",
            "email",
            "image",
            "testimonial_text",
            "rating",
        ]

    def clean(self):
        cleaned_data = super(TestimonialChangeForm, self).clean()
        name = cleaned_data.get("name")
        email = cleaned_data.get("email")
        image = cleaned_data.get("image")
        testimonial_text = cleaned_data.get("testimonial_text")
        rating = cleaned_data.get("rating")

        if not name :
            raise forms.ValidationError(
                "Please add name."
            )
        if not email :
            raise forms.ValidationError(
                "Please add email."
            )
        if not image :
            raise forms.ValidationError(
                "Please add testimonial image."
            )
        if not testimonial_text :
            raise forms.ValidationError(
                "Please add testimonial text."
            )
        if float(rating) < 0.0 or float(rating) > 5.0 :
            raise forms.ValidationError(
                "Rating must be grater than and equal to 0 and less than and equal to 5."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance