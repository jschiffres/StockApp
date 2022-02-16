from django import template
import locale
locale.setlocale( locale.LC_ALL, 'English_United States.1252' )

register = template.Library()

@register.filter
def dollar_format(value):
	return locale.currency( value, grouping=True )