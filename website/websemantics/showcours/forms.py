from django import forms


class QueryForm(forms.Form):
    #your_name = forms.CharField(label='Your name', max_length=100)
    attr = {"class": "form-control", "rows": "7"}
    textarea = forms.CharField(
        label="select * where {\n\t?x ?p ?y\n}", widget=forms.Textarea(attr))


class CursusForm(forms.Form):
    CHOICES = (('AL', 'AL'), ('IAM', 'IAM'), ('SD', 'SD'),
               ('WEB', 'WEB'), ('CASPAR', 'CASPAR'),)
    attr = {"class": "form-control"}
    dominante = forms.CharField(
        widget=forms.Select(choices=CHOICES, attrs=attr))
