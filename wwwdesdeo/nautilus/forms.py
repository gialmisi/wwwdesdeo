from django import forms


class InitializationForm(forms.Form):
    user_iters = forms.IntegerField(
        label="Number of interatinos to run",
        max_value=100,
        initial=10)
    generated_points = forms.IntegerField(
        label="Numbers of points to be generated",
        max_value=100,
        initial=5)
