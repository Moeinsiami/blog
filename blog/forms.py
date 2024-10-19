from django import forms
from blog.models import Comment, Post, User


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


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول", widget=forms.FileInput(attrs={'class': 'form-control'}))
    image2 = forms.ImageField(label="تصویر دوم", widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']


# class LoginForm(forms.Form):
#     username = forms.CharField(required=True, max_length=250)
#     password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),label='پسورد')
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),label='تکرار پسورد')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('پسورد ها مطابقت ندارند!')
        return cd['password2']