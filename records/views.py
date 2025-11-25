from datetime import date, datetime, timedelta

from django.db.models import Count, F, Func, Sum
from django.db.models.functions import TruncMonth, TruncYear
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .datatransfer import get_date_from_the_file as dt
from .forms import ChartFilterForm, ExpenseForm, UploadExpenseForm
from .models import Expense, Sector, Way

# Create your views here.


def index(request):
    """View function for home page of site"""

    # counts of expenses
    num_of_expenses = Expense.objects.all().count()

    # number of kinds of payments method
    num_of_ways = Way.objects.all().count()

    # classified sectors for the statics
    num_of_sectors = Sector.objects.count()

    # Calculate current month's total spending
    current_month_spending = Expense.objects.filter(
        dateinfo__year=datetime.now().year,
        dateinfo__month=datetime.now().month
    ).aggregate(total=Sum('cost'))['total'] or 0

    # Calculate current year's total spending
    current_year_spending = Expense.objects.filter(
        dateinfo__year=datetime.now().year
    ).aggregate(total=Sum('cost'))['total'] or 0

    # Calculate current month's expense count
    monthly_expense_count = Expense.objects.filter(
        dateinfo__year=datetime.now().year,
        dateinfo__month=datetime.now().month
    ).count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_expense": num_of_expenses,
        "num_ways": num_of_ways,
        "num_sectors": num_of_sectors,
        "num_visits": num_visits,
        "monthly_spending": current_month_spending,
        "annual_spending": current_year_spending,
        "monthly_expense_count": monthly_expense_count,
    }

    # check_information_update()

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class ExpenseListView(generic.ListView):
    model = Expense
    paginate_by = 21

    def get_queryset(self):
        return Expense.objects.filter(dateinfo__gte=datetime.now() - timedelta(100000))


class ExpenseDetailView(generic.DetailView):
    model = Expense

    def expense_detail_view(request, id):
        thing = get_object_or_404(Expense, pk=id)

        return render(
            request, "records/expense_detail.html", context={"expense": thing}
        )


class ExpenseCreate(CreateView):
    model = Expense
    form_class = ExpenseForm


class ExpenseUpdate(UpdateView):
    model = Expense
    fields = ["dateinfo", "place", "cost", "way", "sector"]


class ExpenseDelete(DeleteView):
    model = Expense
    success_url = reverse_lazy("expenses")


def importData(request):
    """Import data from the .csv file"""
    if request.method == "POST":
        form = UploadExpenseForm(request.POST)

        if form.is_valid():
            print("============>>>>>>>>>>")
            filepath = form.cleaned_data["csvfile"]
            text = form.cleaned_data["text"]
            dt(filepath)

            return redirect("index")

            # text = form.clean_data['text']
        else:
            print("######################")

        # form = UploadExpenseForm(request.POST, request.FILES)
    else:
        form = UploadExpenseForm()

    return render(request, "import_data.html", {"form": form})


def applyFilter(request):
    """Apply filter to make a chart"""

    if request.method == "POST":
        form = ChartFilterForm(request.POST)

        if form.is_valid():
            print("============>>>>>>>>>>")
            period = form.cleaned_data["period"]
            kind = form.cleaned_data["kind"]
            print("period: {}, kind: {}".format(period, kind))

            return redirect("index")
        else:
            print("######################")
    else:
        form = ChartFilterForm()
        # print(request.GET['kind'])

    return render(request, "charts.html", {"form": form})


class Round(Func):
    function = "ROUND"


def drawDashboard(request):
    table_data = []
    queryset = (
        Expense.objects.filter(dateinfo__year=datetime.now().year)
        .filter(dateinfo__month=datetime.now().month)
        .values("sector__name")
        .order_by("sector")
        .annotate(sector__cost=Round(Sum("cost")))
    )
    # print(queryset)
    return render(
        request,
        "dashboard.html",
        {"thismonth": datetime.now().month, "queryset": queryset},
    )


def getDataset(request):
    labels = []
    datasets = []

    sector_color = {
        "마켓": "red",
        "식사": "orange",
        "여행": "yellow",
        "고정비": "green",
        "교육": "skyblue",
        "병원": "blue",
        "쇼핑": "purple",
        "은행(금전)": "black",
        "주유": "pink",
        "행정": "gray",
    }
    sector_list = ["마켓", "식사", "여행", "고정비", "교육", "병원", "쇼핑", "은행(금전)", "주유", "행정"]

    queryset_sc = (
        Expense.objects.values("dateinfo__year", "dateinfo__month", "sector__name")
        .order_by("dateinfo__year")
        .annotate(sector__cost=Sum("cost"))
    )
    """
    for query in queryset_sc:
        print("{},{} - {} : {}".format(query['dateinfo__year'], query['dateinfo__month'], query['sector__name'], query['sector__cost']))
    """

    queryset_cost = (
        Expense.objects.values("dateinfo__year", "dateinfo__month")
        .order_by("dateinfo__year", "dateinfo__month")
        .annotate(Count("cost"))
    )
    for query in queryset_cost:
        labels.append("{}-{}".format(query["dateinfo__year"], query["dateinfo__month"]))

    for sector in sector_list:
        item = {}
        item["data"] = []
        item["label"] = sector
        item["backgroundColor"] = sector_color[sector]

        for query in queryset_cost:
            # print("now checking {} year {} month with sector name {}".format(query['dateinfo__year'],query['dateinfo__month'], sector))
            if not any(
                sc["dateinfo__year"] == query["dateinfo__year"]
                and sc["dateinfo__month"] == query["dateinfo__month"]
                and sc["sector__name"] == sector
                for sc in queryset_sc
            ):
                item["data"].append(0)
            else:
                [
                    item["data"].append(round(float(sc["sector__cost"]), 2))
                    for sc in queryset_sc
                    if sc["dateinfo__year"] == query["dateinfo__year"]
                    and sc["dateinfo__month"] == query["dateinfo__month"]
                    and sc["sector__name"] == sector
                ]

        datasets.append(item)

    return JsonResponse(
        data={
            "labels": labels,
            "datasets": datasets,
        }
    )


def currencyTrend(request):
    queryset = (
        Expense.objects.filter(dateinfo__year=datetime.now().year)
        .filter(dateinfo__month=datetime.now().month)
        .values("sector__name")
        .order_by("sector")
        .annotate(sector__cost=Round(Sum("cost")))
    )

    return render(
        request,
        "currency.html",
        {"thismonth": datetime.now().month, "queryset": queryset},
    )
