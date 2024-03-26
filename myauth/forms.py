from django import forms
from myauth.models import Profile, User

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('avatar',)

class ProfileUpdateForm(forms.ModelForm):
    """
    Форма обновления данных профиля пользователя
    """
    class Meta:
        model = Profile
        fields = ('bio', 'avatar')
    #
    # def __init__(self, *args, **kwargs):
    #     """
    #     Обновление стилей формы обновления
    #     """
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({
    #             'class': 'form-control',
    #             'autocomplete': 'off'
    #         })