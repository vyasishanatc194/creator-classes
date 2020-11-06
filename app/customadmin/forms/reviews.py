# -*- coding: utf-8 -*-

from django import forms

from user.models import CreatorReview, ClassReview, User

# -----------------------------------------------------------------------------
# Creator Reviews
# -----------------------------------------------------------------------------


class MyCreatorReviewCreationForm(forms.ModelForm):
    """Custom CreatorReviewCreationForm."""

    class Meta:
        model = CreatorReview
        fields = [
            "user",
            "creator",
            "review",
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        print(*args)

    def clean(self):
        cleaned_data = super(MyCreatorReviewCreationForm, self).clean()
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



class MyCreatorReviewChangeForm(forms.ModelForm):
    """Custom CreatorReviewChangeForm."""
    class Meta:
        model = CreatorReview
        fields = (
            "user",
            "creator",
            "review",
            "rating",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        print(*args)
    
    def clean(self):
        cleaned_data = super(MyCreatorReviewChangeForm, self).clean()
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

# -----------------------------------------------------------------------------
# Class Reviews
# -----------------------------------------------------------------------------


class MyClassReviewCreationForm(forms.ModelForm):
    """Custom ClassReviewCreationForm."""

    class Meta:
        model = ClassReview
        fields = [
            "user",
            "creator_class",
            "review",
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        print(*args)

    def clean(self):
        cleaned_data = super(MyClassReviewCreationForm, self).clean()
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



class MyClassReviewChangeForm(forms.ModelForm):
    """Custom ClassReviewChangeForm."""
    class Meta:
        model = ClassReview
        fields = (
            "user",
            "creator_class",
            "review",
            "rating",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        print(*args)
    
    def clean(self):
        cleaned_data = super(MyClassReviewChangeForm, self).clean()
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