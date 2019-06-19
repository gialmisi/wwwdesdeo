from django import forms
from django.forms import formset_factory


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


class AnalyticalProblemInputForm(forms.Form):
    """Documentation for AnalyticalProblemInputForm

    """
    expression = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "row-form-exprs",
            "placeholder": "expression",
        }),
        required=False,
    )

    lower_bound = forms.FloatField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "row-form-bound",
                "placeholder": "low",
            },
        )
    )

    upper_bound = forms.FloatField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "row-form-bound",
                "placeholder": "up",
            },
        )
    )


class AnalyticalProblemInputVariablesForm(forms.Form):
    def __init__(self,
                 symbol,
                 *args,
                 **kwargs):
        super(AnalyticalProblemInputVariablesForm, self).__init__(
            *args, **kwargs)

        self.fields[symbol+"_lower_bound"] = forms.FloatField(
            label=symbol,
            widget=forms.NumberInput(
                attrs={
                    "class": "row-form-quarter",
                    "placeholder": "low",
                },
            )
        )

        self.fields[symbol+"_upper_bound"] = forms.FloatField(
            label="",
            widget=forms.NumberInput(
                attrs={
                    "class": "row-form-quarter",
                    "placeholder": "up",
                },
            )
        )

        self.fields[symbol+"_initial_value"] = forms.FloatField(
            label="",
            widget=forms.NumberInput(
                attrs={
                    "class": "row-form-quarter",
                    "placeholder": "curr",
                },
            )
        )


def VariableFormsFactory(symbols, post=None):
    forms = []
    for symbol in symbols:
        if post is not None:
            form = AnalyticalProblemInputVariablesForm(symbol, {
                symbol+"_lower_bound": post[symbol+"_lower_bound"],
                symbol+"_upper_bound": post[symbol+"_upper_bound"],
                symbol+"_initial_value": post[symbol+"_initial_value"],
            })
        else:
            form = AnalyticalProblemInputVariablesForm(symbol)

        forms.append(form)

    return forms


AnalyticalProblemInputFormSet = formset_factory(AnalyticalProblemInputForm,
                                                extra=1)
