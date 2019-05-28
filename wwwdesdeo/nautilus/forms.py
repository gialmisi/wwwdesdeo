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


class InteractiveForm(forms.Form):
    preferred_point = forms.ChoiceField()
    
    def __init__(self, points, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkj")
        print(points)
        self.fields['preferred_point'].choices = [(0, value[0]) for value in points]


