# -*- coding: utf-8 -*-

from django import forms

from ..models import AdminKeyword

# -----------------------------------------------------------------------------
# AdminKeywords
# -----------------------------------------------------------------------------

class AdminKeywordCreationForm(forms.ModelForm):
    """Custom AdminKeywordCreationForm"""

    class Meta():
        model = AdminKeyword
        fields = [
            "keyword",
            "image"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyword'].required = False
        self.fields['image'].required = False


    def clean(self):
        cleaned_data = super(AdminKeywordCreationForm, self).clean()
        keyword = cleaned_data.get("keyword")
        image = cleaned_data.get("image")

        instance = AdminKeyword.objects.filter(keyword__iexact=keyword).first()
        if instance:
            raise forms.ValidationError(
                "Keyword already exists."
            )

        if not keyword:
            raise forms.ValidationError(
                "Please add keyword."
            )

        if not image:
            raise forms.ValidationError(
                "Please add image."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class AdminKeywordChangeForm(forms.ModelForm):
    """Custom form to change AdminKeyword"""

    class Meta():
        model = AdminKeyword

        fields = [
            "keyword",
            "image"

        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['keyword'].required = False
        self.fields['image'].required = False

    def clean(self):
        cleaned_data = super(AdminKeywordChangeForm, self).clean()
        keyword = cleaned_data.get("keyword")
        image = cleaned_data.get("image")

        if AdminKeyword.objects.filter(keyword__iexact=keyword).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Keyword already exists."
            )
        if not keyword:
            raise forms.ValidationError(
                "Please add keyword."
            )

        if not image:
            raise forms.ValidationError(
                "Please add image."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance