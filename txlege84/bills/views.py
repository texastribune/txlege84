from django.views.generic import DetailView

from bills.models import Bill


class BillDetail(DetailView):
    model = Bill
    template_name = 'pages/bill.html'
