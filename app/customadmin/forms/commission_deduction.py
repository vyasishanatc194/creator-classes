# -*- coding: utf-8 -*-

from django import forms

from ..models import CreatorClassCommission

# -----------------------------------------------------------------------------
# AdminKeywords
# -----------------------------------------------------------------------------

class CommissionCreationForm(forms.ModelForm):
    """Custom CommissionCreationForm"""

    class Meta():
        model = CreatorClassCommission
        fields = [
            "affiliation_deduction",
            "creator_class_deduction",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['affiliation_deduction'].required = False
        self.fields['creator_class_deduction'].required = False


    def clean(self):
        cleaned_data = super(CommissionCreationForm, self).clean()
        affiliation_deduction = cleaned_data.get("affiliation_deduction")
        creator_class_deduction = cleaned_data.get("creator_class_deduction")

        instance = CreatorClassCommission.objects.all().first()
        if instance:
            raise forms.ValidationError(
                "Commissions already exists."
            )

        if not affiliation_deduction:
            raise forms.ValidationError(
                "Please add affiliation deduction percentage."
            )
        if not creator_class_deduction:
            raise forms.ValidationError(
                "Please add creator classes deduction percentage."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class CommissionChangeForm(forms.ModelForm):
    """Custom form to change CommissionChangeForm"""

    class Meta():
        model = CreatorClassCommission

        fields = [
            "affiliation_deduction",
            "creator_class_deduction",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['affiliation_deduction'].required = False
        self.fields['creator_class_deduction'].required = False

    def clean(self):
        cleaned_data = super(CommissionChangeForm, self).clean()
        affiliation_deduction = cleaned_data.get("affiliation_deduction")
        creator_class_deduction = cleaned_data.get("creator_class_deduction")

        if not affiliation_deduction:
            raise forms.ValidationError(
                "Please add affiliation deduction percentage."
            )
        if not creator_class_deduction:
            raise forms.ValidationError(
                "Please add creator classes deduction percentage."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance