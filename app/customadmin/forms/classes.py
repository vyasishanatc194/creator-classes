# -*- coding: utf-8 -*-

from django import forms

from creator.models import CreatorClass, ClassKeyword, ClassCovers

# -----------------------------------------------------------------------------
# Creator Classes
# -----------------------------------------------------------------------------


class MyCreatorClassCreationForm(forms.ModelForm):
    """Custom CreatorCreationForm."""

    class Meta:
        model = CreatorClass
        fields = [
            "creator",
            "title",
            "thumbnail_file",
            "class_file",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance



class MyCreatorClassChangeForm(forms.ModelForm):
    """Custom CreatorChangeForm."""
    class Meta:
        model = CreatorClass
        fields = (
            "creator",
            "title",
            "thumbnail_file",
            "class_file",
        )

# -----------------------------------------------------------------------------
# Creator Keywords
# -----------------------------------------------------------------------------

class ClassKeywordCreationForm(forms.ModelForm):
    """Custom form to create Class Keyword"""

    class Meta():
        model = ClassKeyword
        fields = [
            "keyword",
            "creator_class",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class ClassKeywordChangeForm(forms.ModelForm):
    """Custom form to change Class Keyword"""

    class Meta():
        model = ClassKeyword

        fields = [
            "keyword",
            "creator_class",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance

# -----------------------------------------------------------------------------
# Creator Covers
# -----------------------------------------------------------------------------

class ClassCoversCreationForm(forms.ModelForm):
    """Custom form to create Class Covers"""

    class Meta():
        model = ClassCovers
        fields = [
            "covers",
            "creator_class",
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class ClassCoversChangeForm(forms.ModelForm):
    """Custom form to change Class Covers"""

    class Meta():
        model = ClassCovers

        fields = [
            "covers",
            "creator_class",
        ]
    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance