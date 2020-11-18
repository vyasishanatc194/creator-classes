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
        ]

    def __init__(self, *args, **kwargs):
        # self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        print(*args)
        self.fields['keyword'].required = False


    def clean(self):
        cleaned_data = super(AdminKeywordCreationForm, self).clean()
        keyword = cleaned_data.get("keyword")

        instance = AdminKeyword.objects.filter(keyword__iexact=keyword).first()
        if instance:
            raise forms.ValidationError(
                "Keyword already exists."
            )

        if not keyword:
            raise forms.ValidationError(
                "Please add keyword."
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
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)
        self.fields['keyword'].required = False

    def clean(self):
        cleaned_data = super(AdminKeywordChangeForm, self).clean()
        keyword = cleaned_data.get("keyword")
        
        if AdminKeyword.objects.filter(keyword__iexact=keyword).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Keyword already exists."
            )
        if not keyword:
            raise forms.ValidationError(
                "Please add keyword."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance