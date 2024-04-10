from django import forms
from . import models as md


class CreateListingForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={
                "class": "form-control"
            }
        )
    )
    price = forms.DecimalField(
        label="Starting price",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    category = forms.ModelChoiceField(
        queryset=md.Category.objects.all(),
        required=False,
        empty_label="No Category",
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        )
    )
    image_url = forms.URLField(
        label="Image Url",
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control"
            }
        ),
    )


class CommentForm(forms.Form):
    content = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Leave a comment"
            }
        )
    )


class BidForm(forms.Form):
    price = forms.DecimalField(
        label="Price",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control"
            }
        )
    )
