from django import forms


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=100)
    slug = forms.SlugField(max_length=110)
    description = forms.CharField(widget=forms.Textarea, required=False)
    icon = forms.CharField(max_length=100, required=False)
    base_price = forms.DecimalField(max_digits=8, decimal_places=2)
