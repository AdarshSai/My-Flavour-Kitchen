from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory
from .models import Pizza
from sendsms import api
from sendsms.message import SmsMessage
from sendsms.backends.base import BaseSmsBackend
# import some.sms.delivery.api

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method == 'POST':
        created_pizza_pk = None
        filled_form = PizzaForm(request.POST)
        if filled_form.is_valid():
            created_pizza = filled_form.save()
            created_pizza_pk = created_pizza.id
            note = 'Thanks for ordering! Your %s %s and %s pizza is on its way!' %(filled_form.cleaned_data['size'], filled_form.cleaned_data['Main_Course'], filled_form.cleaned_data['Side_Dish'],)
            filled_form = PizzaForm()
            SENDSMS_BACKEND = 'myapp.mysmsbackend.SmsBackend'
            api.send_sms(body='I can text', from_phone='+12263406180', to=['+12263406180'])
            message = SmsMessage(body='lolcats make me hungry', from_phone='+12263406180', to=['+12263406180'])
            message.send()
        else:
            note = 'Order was not created, please try again'
        new_form = PizzaForm()
        return render(request, 'pizza/order.html', {'multiple_form':multiple_form, 'pizzaform':filled_form, 'note':note, 'created_pizza_pk':created_pizza_pk})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'multiple_form':multiple_form, 'pizzaform':form})
def Menu_item(request):
    #multiple_form = MultiplePizzaForm()
    return render(request, 'pizza/Menu_item.html')# {'multiple_form':multiple_form, 'pizzaform':form})
def edit_order(request,pk):
    pizza = Pizza.objects.get(pk=pk)
    form = PizzaForm(instance=pizza)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST, instance=pizza)
        if filled_form.is_valid():
            filled_form.save()
            form = filled_form
            note = 'Your order has been processed.'
            return render(request, 'pizza/edit_order.html', {'pizzaform':form, 'pizza':pizza, 'note':note})
    return render(request, 'pizza/edit_order.html', {'pizzaform':form, 'pizza':pizza})
# class AwesomeSmsBackend(BaseSmsBackend):
#     def send_messages(self, messages):
#         for message in messages:
#             for to in message.to:
#                 try:
#                     some.sms.delivery.api.send(
#                         message=message.body,
#                         from_phone=message.from_phone,
#                         to_phone=to,
#                         flashing=message.flash
#                     )
#                 except:
#                     if not self.fail_silently:
#                         raise

def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        number_of_pizzas = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == "POST":
        filled_formset = PizzaFormSet(request.POST)
        if(filled_formset.is_valid()):
            for form in filled_formset:
                print(form.cleaned_data['Main_Course'])
            note = 'Pizzas have been ordered!'
        else:
            note = 'Order was not created, please try again'


        return render(request, 'pizza/pizzas.html', {'note':note, 'formset':formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset':formset})
