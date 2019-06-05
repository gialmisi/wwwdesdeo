from django import forms


class InitializationForm(forms.Form):
    def __create_form(self, fields, label, field_labels=None):
        if not field_labels:
            field_labels = fields
        return forms.CharField(
            label=label,
            widget=forms.Select(
                choices=[choice for choice in zip(
                    fields,
                    field_labels)]))

    def __init__(
            self,
            available_methods,
            available_optimizers,
            problems,
            *args,
            **kwargs):
        super(InitializationForm, self).__init__(*args, **kwargs)

        self.__available_optimizers = available_optimizers
        self.__problems = problems

        self.fields["interactive_method"] = self.__create_form(
            available_methods,
            "Interactive method")
        self.fields["optimizer"] = self.__create_form(
            available_optimizers,
            "Optimizer")
        self.fields["problem"] = self.__create_form(
            problems,
            "Problem to be solved")


class MethodInitializationForm(forms.Form):
    def __init__(self,
                 requirements,
                 *args,
                 **kwargs):
        super(MethodInitializationForm, self).__init__(*args, **kwargs)

        for requirement in requirements:
            self.fields[requirement] = forms.FloatField(label=requirement)


class IterationForm(forms.Form):
    def __init__(self,
                 choices,
                 *args,
                 **kwargs):
        super(IterationForm, self).__init__(*args, **kwargs)

        labeled_choices = zip(choices, range(len(choices)))
        choice_field = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=labeled_choices,
            label="")
        self.fields["choice"] = choice_field
