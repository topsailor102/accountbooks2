from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Count, Sum

from .models import Expense, Sector, Way


def check_csvfile(file):
    if file.split(".")[-1] != "csv":
        raise forms.ValidationError(_("file format is not expected!"))


class UploadExpenseForm(forms.Form):
    csvfile = forms.FileField(validators=[check_csvfile])
    text = forms.CharField(widget=forms.Textarea)


my_choices1 = (
    ("WY", "Wonyoung"),
    ("YO", "Yunok"),
    ("SH", "Seunghu"),
    ("SY", "Seungyeon"),
)
my_choices2 = (
    ("All", "All"),
    ("L3", "Last 3 months"),
    ("L6", "Last 6 months"),
    ("T", "This month"),
)
my_choices3 = (
    ("2019-9", "2019-9"),
    ("2019-10", "2019-10"),
    ("2019-11", "2019-11"),
    ("2019-12", "2019-12"),
    ("2020-1", "2020-1"),
    ("2020-2", "2020-2"),
    ("2020-3", "2020-3"),
    ("2020-4", "2020-4"),
    ("2020-5", "2020-5"),
)


def get_choice1():
    choices = [
        ("999", "모두"),
    ]
    queryset_cost = Sector.objects.all()

    for query in queryset_cost:
        choices.append(("{}".format(query.id), "{}".format(query)))

    print(tuple(choices))
    return tuple(choices)


def get_choice2():
    choices = []
    queryset_cost = (
        Expense.objects.values("dateinfo__year", "dateinfo__month")
        .order_by("dateinfo__year")
        .annotate(Count("cost"))
    )
    for query in queryset_cost:
        choices.append(
            (
                "{}-{}".format(query["dateinfo__year"], query["dateinfo__month"]),
                "{}-{}".format(query["dateinfo__year"], query["dateinfo__month"]),
            )
        )

    print(tuple(choices))
    return tuple(choices)


class ChartFilterForm(forms.Form):
    kind = forms.MultipleChoiceField()
    period = forms.ChoiceField()

    def __init__(self, *arg, **kwargs):
        super(ChartFilterForm, self).__init__(*arg, **kwargs)
        self.fields["kind"].choices = get_choice1()
        # self.fields["kind"].widget.attrs["size"] = "11"
        self.fields["kind"].initial = [
            "999",
        ]
        self.fields["period"].choices = my_choices2


class ExpenseForm(forms.ModelForm):
    """Custom form for Expense with date picker widget"""
    
    class Meta:
        model = Expense
        fields = '__all__'
        widgets = {
            'dateinfo': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        # Set default date to most recent expense date
        if not self.instance.pk:  # Only for new instances
            latest_expense = Expense.objects.order_by('-dateinfo').first()
            if latest_expense and latest_expense.dateinfo:
                self.fields['dateinfo'].initial = latest_expense.dateinfo
        
        # Set default summary text
        if not self.instance.pk and not self.initial.get('summary'):
            self.fields['summary'].initial = "Describe the details or keyword for spending"
            
        # Exclude 'ING' from payment methods as requested
        if 'way' in self.fields:
            self.fields['way'].queryset = Way.objects.exclude(name='ING')

