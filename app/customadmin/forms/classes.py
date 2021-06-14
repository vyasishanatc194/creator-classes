# -*- coding: utf-8 -*-

from django import forms

from creator.models import CreatorClass, ClassKeyword, ClassCovers, ClassMaterial, Creator

# -----------------------------------------------------------------------------
# Creator Classes
# -----------------------------------------------------------------------------
class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class MyCreatorClassCreationForm(forms.ModelForm):
    """Custom CreatorCreationForm."""
    
    class_file = forms.CharField(required=False)

    class Meta:
        model = CreatorClass
        fields = [
            "creator",
            "title",
            "thumbnail_file",
            "class_file",
            "class_description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')
        self.fields['creator'].required = False

    def clean(self):
        cleaned_data = super(MyCreatorClassCreationForm, self).clean()
        creator = cleaned_data.get("creator")
        title = cleaned_data.get("title")
        thumbnail_file = cleaned_data.get("thumbnail_file")
        class_file = cleaned_data.get("class_file")
        class_description = cleaned_data.get("class_description")

        if not creator :
            raise forms.ValidationError(
                "Please select creator."
            )
        if not title :
            raise forms.ValidationError(
                "Please add class title."
            )
        if not thumbnail_file :
            raise forms.ValidationError(
                "Please add thumbnail file for class."
            )
        if not class_file :
            raise forms.ValidationError(
                "Please add class file."
            )

        if not class_description:
            raise forms.ValidationError(
                "Please add class description."
            )

    def save(self, commit=True):
        instance = super().save()
        if commit:
            instance.save()
        return instance



class MyCreatorClassChangeForm(forms.ModelForm):
    """Custom CreatorChangeForm."""

    class_file = forms.CharField(required=False)

    class Meta:
        model = CreatorClass
        fields = (
            "creator",
            "title",
            "thumbnail_file",
            "class_file",
            "class_description",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creator'].queryset = Creator.objects.filter(status='ACCEPT')

    def clean(self):
        cleaned_data = super(MyCreatorClassChangeForm, self).clean()
        creator = cleaned_data.get("creator")
        title = cleaned_data.get("title")
        thumbnail_file = cleaned_data.get("thumbnail_file")
        class_file = cleaned_data.get("class_file")
        class_description = cleaned_data.get("class_description")

        if not creator :
            raise forms.ValidationError(
                "Please select creator"
            )
        if not title :
            raise forms.ValidationError(
                "Please add class title."
            )
        if not thumbnail_file :
            raise forms.ValidationError(
                "Please add thumbnail file for class."
            )
        if not class_file :
            raise forms.ValidationError(
                "Please add class file."
            )

        if not class_description:
            raise forms.ValidationError(
                "Please add class description."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()

        return instance

# -----------------------------------------------------------------------------
# Class Keywords
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
# Class Covers
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


# -----------------------------------------------------------------------------
# Class Materials
# -----------------------------------------------------------------------------

class ClassMaterialCreationForm(forms.ModelForm):
    """Custom form to create Class Covers"""

    class Meta():
        model = ClassMaterial
        fields = [
            "creator_class",
            "class_material",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance


class ClassMaterialChangeForm(forms.ModelForm):
    """Custom form to change Class Covers"""

    class Meta():
        model = ClassMaterial

        fields = [
            "creator_class",
            "class_material",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance