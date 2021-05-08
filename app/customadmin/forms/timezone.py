from django import forms

from ..models import AvailableTimezone


class TimezoneCreateForm(forms.ModelForm):
    class Meta:
        model = AvailableTimezone
        fields = [
                    'tz'
                ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(TimezoneCreateForm, self).clean()
        tz = cleaned_data.get('tz')
        if not tz:
            raise forms.ValidationError(
                "Please add Timezone."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance