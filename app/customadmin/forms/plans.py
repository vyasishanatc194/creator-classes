# -*- coding: utf-8 -*-

from django import forms

from ..models import Plan, PlanCover
# -----------------------------------------------------------------------------
# Creator's OneToOne Sessions
# -----------------------------------------------------------------------------


class PlanCreationForm(forms.ModelForm):
    """Custom OneToOneSessionCreationForm."""

    class Meta:
        model = Plan
        fields = [
            "name",
            "plan_amount",
            "duration_in_months",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)

    def clean(self):
        cleaned_data = super(PlanCreationForm, self).clean()
        name = cleaned_data.get("name")
        plan_amount = cleaned_data.get("plan_amount")
        duration_in_months = cleaned_data.get("duration_in_months")
        instance = Plan.objects.filter(name=name, plan_amount=plan_amount,duration_in_months=duration_in_months).first()

        if instance:
            raise forms.ValidationError(
                "Plan already exists."
            )

        if not name:
            raise forms.ValidationError(
                "Please enter plan name."
            )
        if float(plan_amount) < 0.0:
            raise forms.ValidationError(
                "Amount must be grater than zero."
            )
        if float(duration_in_months) < 1:
            raise forms.ValidationError(
                "Duration of Plan is more than 1."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class PlanChangeForm(forms.ModelForm):
    """Custom OneToOneSessionChangeForm."""
    class Meta:
        model = Plan
        fields = (
            "name",
            "plan_amount",
            "duration_in_months",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)
        # self.fields['creator'].required = False


    def clean(self):
        cleaned_data = super(PlanChangeForm, self).clean()
        name = cleaned_data.get("name")
        plan_amount = cleaned_data.get("plan_amount")
        duration_in_months = cleaned_data.get("duration_in_months")

        if Plan.objects.filter(name=name, plan_amount=plan_amount, duration_in_months=duration_in_months).exclude(pk=self.instance.id).count() > 0:
            raise forms.ValidationError(
                "Plan already exists."
            )

        if not name:
            raise forms.ValidationError(
                "Please enter plan name."
            )
        if float(plan_amount) < 0.0:
            raise forms.ValidationError(
                "Amount must be grater than zero."
            )
        if float(duration_in_months) < 1:
            raise forms.ValidationError(
                "Duration of Plan is more than 1."
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

# -----------------------------------------------------------------------------
# Creator's TimeSlots
# -----------------------------------------------------------------------------


class PlanCoverCreationForm(forms.ModelForm):
    """Custom TimeSlotCreationForm."""

    class Meta:
        model = PlanCover
        fields = [
            "covers",
            "plan"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)

    # def clean(self):
    #     cleaned_data = super(PlanCoverCreationForm, self).clean()
    #     slot_datetime = cleaned_data.get("slot_datetime")
        
    #     today_date = timezone.now()
    #     if today_date > slot_datetime:
    #         raise forms.ValidationError(
    #             "Please add valid date."
    #         )

    #     if not slot_datetime:
    #         raise forms.ValidationError(
    #             "Please add slot date time."
    #         )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance



class PlanCoverChangeForm(forms.ModelForm):
    """Custom TimeSlotChangeForm."""
    class Meta:
        model = PlanCover
        fields = (
            "covers",
            "plan",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(*args)

    # def clean(self):
    #     cleaned_data = super(PlanCoverCreationForm, self).clean()
    #     slot_datetime = cleaned_data.get("slot_datetime")

    #     if not slot_datetime:
    #         raise forms.ValidationError(
    #             "Please add slot date time."
    #         )
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance