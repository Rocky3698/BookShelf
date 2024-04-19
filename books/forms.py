from django import forms
from .models import Review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        labels={
            'text':'Write your Review',
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}) 
        }