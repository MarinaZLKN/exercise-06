from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms

class RoomAddForm(forms.Form):
    name = forms.CharField(label="Group name", required=True)

    def __init__(self, *args, **kwargs):
        # this will throw an exception if the class was initialized without "user_list" argument
        self.user_list = kwargs.pop('user_list')
        super(RoomAddForm, self).__init__(*args, **kwargs)

        # we are initializing this field here because we are using data passed from view: user_list
        self.fields['room_members'] = forms.ModelMultipleChoiceField(
            queryset=self.user_list,
            required=True,
            widget=forms.CheckboxSelectMultiple
        )

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Row(
                Column('name')
            ),
            Row(
                Column('room_members')
            ),
            Submit('submit', 'Create')
        )
