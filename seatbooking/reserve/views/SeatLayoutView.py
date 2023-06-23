from django.views import generic

class SeatLayout(generic.TemplateView):
    template_name = 'reserve/seat_layout.html'