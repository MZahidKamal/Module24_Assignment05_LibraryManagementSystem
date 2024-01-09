from django import forms
from .models import BookReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['review_text']
        labels = {'review_text': 'Write your review here'}
        help_texts = {'review_text': 'Your review should be at least 50 characters long.'}

    def clean_review_text(self):
        review_text = self.cleaned_data['review_text']
        if len(review_text) < 50:
            raise forms.ValidationError("Please write a review with at least 50 characters.")
        return review_text
