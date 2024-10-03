from django import forms
from blog.models import Comment


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش'),
    )

    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField()
    phone = forms.CharField(max_length=11, required=True)
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("name error")
            else:
                return name


class CommentForm(forms.ModelForm):
    def clean_name(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست!")
            else:
                return phone

    class Meta:
        model = Comment
        fields = ['name', 'body']


class SearchForm(forms.Form):
    query = forms.CharField()