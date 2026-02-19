from django import forms
import pytz

class UpdateUserInfo(forms.Form):
  email = forms.EmailField(label="Email", max_length=150)
  timezone = forms.ChoiceField(choices=[(tz, tz) for tz in pytz.all_timezones], label='Prefered time zone')