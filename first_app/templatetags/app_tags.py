from django import template
from first_app.models import Number

register=template.Library()


@register.filter
def quantity(value):
	orders=Number.objects.filter(Items=value)
	return orders


@register.filter
def multiply(value,arg):
	value=int(value)
	arg=int(arg)
	return value*arg	


@register.filter
def total(value):
	orders=Number.objects.filter(Items=value)
	pending=0
	for i in orders:
		pending=pending+(i.Order.Price*i.Quantity)
	return pending	



