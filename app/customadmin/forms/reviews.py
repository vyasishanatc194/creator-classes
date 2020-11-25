# -*- coding: utf-8 -*-

from django import forms

from user.models import CreatorReview, ClassReview, User
from creator.models import Creator

# -----------------------------------------------------------------------------
# Creator Reviews
# -----------------------------------------------------------------------------


class MyCreatorReviewCreationForm(forms.ModelForm):
    """Custom CreatorReviewCreationForm."""

    class Meta:
        model = CreatorReview
        fields = [
            "creator",
            "user",
            "review",
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False
        self.fields['user'].required = False

    def clean(self):
        cleaned_data = super(MyCreatorReviewCreationForm, self).clean()
        creator = cleaned_data.get("creator")
        user = cleaned_data.get("user")
        rating = cleaned_data.get("rating")
        review = cleaned_data.get("review")

        instance = CreatorReview.objects.filter(creator=creator, user=user).first()
        if instance:
            raise forms.ValidationError(
                "Category Review already exists with selected user."
            )

        if not creator :
            raise forms.ValidationError(
                "Please select creator."
            )
        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not review :
            raise forms.ValidationError(
                "Please add review for creator."
            )
        if float(rating) < 0.0 or float(rating) > 5.0 :
            raise forms.ValidationError(
                "Rating must be grater then and equal to 0 and less than and equal to 5."
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
            "creator",
            "user",
            "review",
            "rating",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False
        self.fields['user'].required = False

    def clean(self):
        cleaned_data = super(MyCreatorReviewChangeForm, self).clean()
        creator = cleaned_data.get("creator")
        user = cleaned_data.get("user")
        rating = cleaned_data.get("rating")
        review = cleaned_data.get("review")

        if CreatorReview.objects.filter(creator=creator, user=user).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Creator review already exists with selected user."
            )

        if not creator :
            raise forms.ValidationError(
                "Please select creator."
            )
        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not review :
            raise forms.ValidationError(
                "Please add review for creator."
            )

        if float(rating) < 0.0 or float(rating) > 5.0 :
            raise forms.ValidationError(
                "Rating must be grater then and equal to 0 and less than and equal to 5."
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
            "creator_class",
            "user",
            "review",
            "rating",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['creator_class'].required = False
        self.fields['user'].required = False

    def clean(self):
        cleaned_data = super(MyClassReviewCreationForm, self).clean()
        creator_class = cleaned_data.get("creator_class")
        user = cleaned_data.get("user")
        rating = cleaned_data.get("rating")
        review = cleaned_data.get("review")

        instance = ClassReview.objects.filter(creator_class=creator_class, user=user).first()
        if instance:
            raise forms.ValidationError(
                "Class Review already exists with selected user."
            )

        if not creator_class :
            raise forms.ValidationError(
                "Please select creator class."
            )
        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not review :
            raise forms.ValidationError(
                "Please add review for creator."
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

class MyClassReviewChangeForm(forms.ModelForm):
    """Custom ClassReviewChangeForm."""
    class Meta:
        model = ClassReview
        fields = (
            "creator_class",
            "user",
            "review",
            "rating",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_creator=False).exclude(username='admin')
        self.fields['creator_class'].required = False
        self.fields['user'].required = False

    def clean(self):
        cleaned_data = super(MyClassReviewChangeForm, self).clean()
        creator_class = cleaned_data.get("creator_class")
        user = cleaned_data.get("user")
        rating = cleaned_data.get("rating")
        review = cleaned_data.get("review")

        if ClassReview.objects.filter(creator_class=creator_class, user=user).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Class review already exists with selected user."
            )

        if not creator_class :
            raise forms.ValidationError(
                "Please select creator class."
            )
        if not user :
            raise forms.ValidationError(
                "Please select user."
            )
        if not review :
            raise forms.ValidationError(
                "Please add review for creator."
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