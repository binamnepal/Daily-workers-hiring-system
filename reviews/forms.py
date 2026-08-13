from django import forms


class CreateReviewForm(forms.Form):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)])
    comment = forms.CharField(widget=forms.Textarea, required=False)
