from django.db import models
import uuid


class CarModel(models.Model):
    model = models.CharField('Auto modelis', max_length=15)
    make = models.CharField('Auto marke', max_length=15)
    year = models.DateField('Pagaminimo metai')
    engine = models.CharField('Variklis', max_length=20)
    LOAN_STATUS = (
        ('b', 'Benzinas'),
        ('d', 'Dyzelinas'),
        ('g', 'Dujos'),
        ('e', 'Elektra')
    )

    fuel_type = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        help_text='Degalu tipas'
    )

    class Meta:
        verbose_name = "Auto Modelis"
        verbose_name_plural = "Auto Modeliai"

    def __str__(self):
        return f"{self.model} {self.make} {self.year} {self.engine} {self.fuel_type}"




class Client(models.Model):
    f_name = models.CharField('Vardas', max_length=20)
    l_name = models.CharField('Pavarde', max_length=20)

    class Meta:
        verbose_name = "Klientas"
        verbose_name_plural = "Klientai"

    def __str__(self):
        return f"{self.f_name} {self.l_name}"


class Car(models.Model):
    i_nr = models.CharField('Auto nr', max_length=10, blank=True)
    vin = models.CharField('VIN nr', blank=True, max_length=17, help_text='17 Simboliu <a href="https://en.wikipedia.org/wiki/Vehicle_identification_number">VIN kodas</a>')
    car_mod = models.ForeignKey('CarModel', null=True, blank=True, on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

    def __str__(self):
        return f"{self.i_nr} {self.car_mod.model} {self.car_mod.make} {self.client.f_name}"



class Services(models.Model):

    name = models.CharField('Paslaugos pav.', max_length=50)
    price = models.FloatField('Kaina uz paslauga')
    car = models.ForeignKey('Car', blank=True, on_delete=models.SET_NULL, null=True)


    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return f"{self.name} {self.price}"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField('Data')
    price_sum = models.FloatField('Uzsakymu kaina', blank=True, null=True)
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True,  blank=True)

    def display_service_rows_quant(self):
        quantities = [str(row.quantity) for row in self.orders.all()]
        return ', '.join(quantities)

    def display_service_rows_prices(self):
        prices = [str(row.price) for row in self.orders.all()]
        return ', '.join(prices)

    def display_services(self):
        return ', '.join(serv_name.service.name for serv_name in self.orders.all())

    display_service_rows_quant.short_description = "Paslaugu kiekis"
    display_service_rows_prices.short_description = "Paslaugu kaina"
    display_services.short_description = "Paslaugos pav."

    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"


    def __str__(self):
        return f"{self.date} {self.price_sum} {self.car.i_nr} {self.car.client.f_name}"



class ServicesRows(models.Model):
    quantity = models.IntegerField('Paslaugu kiekis')
    price = models.IntegerField('Kaina', blank=True, null=True)
    service = models.ForeignKey('Services', on_delete=models.SET_NULL, null=True, related_name='servicesrows_set')
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, related_name='orders')

    class Meta:
        verbose_name = "Uzsakymu eilute"
        verbose_name_plural = "Uzsakymu eilutes"



    def __str__(self):
        return f"{self.quantity} {self.service.name} {self.service.price}"



