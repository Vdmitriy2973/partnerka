from django import forms

class ApiSettingsForm(forms.Form):
    api_key = forms.CharField(
        label='API ключ',
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered join-item flex-1',
            'id': 'api_key',
            'type': 'password'  
        })
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and not self.data:
            self.fields['api_key'].initial = self.request.user.advertiserprofile.api_key