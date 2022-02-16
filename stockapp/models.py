from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField

# Create your models here.
class Stock(models.Model):
	ticker = models.CharField(max_length=6, primary_key=True) 
	company = models.CharField(max_length=100)
	
	def __str__(self):
		return self.ticker


class Portfolio(models.Model):
	title = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add=True)
	value = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
	cash = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
	portfolio_return = models.FloatField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class Transaction(models.Model):
	ticker = models.CharField(max_length=6)
	name = models.CharField(max_length=120)
	price = models.FloatField()
	quantity = models.IntegerField(validators=[MinValueValidator(1)])
	shares_remaining = models.IntegerField(default=0, validators=[MinValueValidator(0)])
	Buy = 'Buy'
	Sell = 'Sell'
	transaction_type = models.CharField(max_length=4, choices=[(Buy,'Buy'),(Sell,'Sell')])
	buyvalue = models.FloatField(default=0)
	sellvalue = models.FloatField(default=0)
	date = models.DateTimeField(auto_now_add=True)
	portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


	def __str__(self):
		return f"{self.portfolio} - {self.transaction_type} {self.ticker}"

class Holding(models.Model):
	ticker = models.CharField(max_length=6)
	name = models.CharField(max_length=120)
	avg_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
	shares = models.IntegerField(validators=[MinValueValidator(0)])
	portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)


class TransactionTwo(models.Model):
	ticker = models.CharField(max_length=6)
	name = models.CharField(max_length=120)
	price = models.FloatField()
	quantity = models.IntegerField(validators=[MinValueValidator(1)])
	Buy = 'Buy'
	Sell = 'Sell'
	transaction_type = models.CharField(max_length=4, choices=[(Buy,'Buy'),(Sell,'Sell')])
	date = models.DateTimeField(auto_now_add=True)