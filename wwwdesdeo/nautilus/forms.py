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
            examples,
            *args,
            **kwargs):

        super(InitializationForm, self).__init__(*args, **kwargs)

        self.__available_optimizers = available_optimizers
        self.__examples = examples

        self.fields["interactive_method"] = self.__create_form(
            available_methods,
            "Interactive method")
        self.fields["optimizer"] = self.__create_form(
            available_optimizers,
            "Optimizer")
        self.fields["examples"] = self.__create_form(
            examples,
            "Pre-defined example")
