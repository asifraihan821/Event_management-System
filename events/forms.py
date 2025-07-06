from django import forms

class EventForm(forms.Form): 
    name = forms.CharField(max_length=300, label='Event Name')
    category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label= "Category")
    participants = forms.IntegerField()
    date = forms.DateField(widget=forms.SelectDateWidget)

    def __init__(self,*args,**kwargs):
        category = kwargs.pop('category', [])
        super().__init__(*args,**kwargs)
        self.fields['category'].choices = [
            (cat.id, cat.name) for cat in category]