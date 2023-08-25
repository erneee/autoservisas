from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import csv
from django.views import generic
from django.db.models import Q
from .models import CarModel, Car, Client, Services, ServicesRows, Order


def index(request):
    numb_of_services_count = Services.objects.all().count()
    numb_of_services = Services.objects.all()
    numb_of_orders = Order.objects.all().count()
    numb_of_orders_display = Order.objects.all()
    num_of_clients = Client.objects.all().count()
    num_of_clients_display = Client.objects.all()
    num_of_cars = Car.objects.all().count()
    numb_pertol_cars = CarModel.objects.filter(fuel_type__exact='d').count()

    context_t = {
        'numb_of_services_count_t': numb_of_services_count,
        'numb_of_services_t': numb_of_services,
        'numb_of_orders_t': numb_of_orders,
        'numb_of_orders_display_t': numb_of_orders_display,
        'num_of_clients_t': num_of_clients,
        'num_of_clients_display_t': num_of_clients_display,
        'num_of_cars_t': num_of_cars,
        'numb_pertol_cars_t': numb_pertol_cars,

    }

    return render(request, 'index.html', context=context_t)


def auto_kiekis(request):
    num_of_cars = Car.objects.all()

    context_t = {
        'num_of_cars_t': num_of_cars,
    }

    return render(request, 'auto_kiekis.html', context=context_t)


def customer_car(request, car_id):
    singe_car = get_object_or_404(Car, pk=car_id)
    context_t = {
        'singe_car_t': singe_car,
    }

    return render(request, 'customer_car.html', context_t)


def services(request):
    numb_of_services = Services.objects.all()
    context_t ={
        'numb_of_services_t': numb_of_services,
    }
    return render(request, 'services.html', context_t)


class  OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'


def search(request):
    query = request.GET.get('search_text')
    search_results = Car.objects.filter(
        Q(car_mod__model__icontains=query) |
        Q(client__f_name__icontains=query) |
        Q(client__l_name__icontains=query) |
        Q(vin__icontains=query) |
        Q(i_nr__icontains=query)
    )
    context_t = {
        'query_t': query,
        'search_results_t': search_results,
    }

    return  render(request, 'search.html', context_t)



