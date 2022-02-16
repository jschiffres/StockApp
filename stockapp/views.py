from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone
from .forms import CreateUserForm, CreatePortfolioForm, BuyForm, SellForm, EditPortfolioForm
from .models import Stock, Portfolio, Transaction, Holding
from django.db.models import Sum, Avg, F, FloatField
from decimal import Decimal
from newsapi import NewsApiClient
import plotly.express as px
import plotly.graph_objects as go
import datetime
import yfinance as yf



# Create your views here.
def home(request):
	ticker = request.GET.get('stock_ticker')
	if ticker != '' and ticker is not None:
		return redirect('stockpage', ticker)
	else:
		#NEWS FEED
		today = datetime.date.today()
		enddate = today - datetime.timedelta(days=0)
		newsapi = NewsApiClient(api_key='3022ab97a59645feb6e11dca8cb54c4a')
		get_articles = newsapi.get_everything(q='stock market',sources='the-wall-street-journal,bloomberg',domains='wsj.com,bloomberg.com',from_param=today.strftime("%Y-%m-%d"),to=enddate.strftime("%Y-%m-%d"),language='en',sort_by='relevancy',page_size=6)
		articles = get_articles['articles']
		i = 0
		articles_list = []
		while i < len(articles):
			source = (articles[i]['source']['name'])
			author = (articles[i]['author'])
			title = (articles[i]['title'])
			content = (articles[i]['content'][:180]+"...")
			date = (articles[i]['publishedAt'][:10])
			url = (articles[i]['url'])
			articles_list.append({"source":source, "author":author, "title":title, "content":content, "date":date, "url":url})
			i += 1

		#LEADERBOARD
		portfolios = Portfolio.objects.all().order_by('-portfolio_return')[:10]

		#MARKET SUMMARY
		indexes = [{"Ticker":"DOW"}, {"Ticker":"S&P 500"}, {"Ticker":"NASDAQ"}]
		tickers = ["^DJI", "^GSPC", "QQQ"]
		loop = 0
		for i in tickers:
			info = yf.Ticker(i).info
			indexes[loop]['change'] = ((info['ask']-info['regularMarketPreviousClose'])/info['regularMarketOpen'])*100
			indexes[loop]['ask'] = info['ask']
			loop += 1
		print(indexes)
		return render(request, 'stockapp/home.html', {'portfolios':portfolios,'articles':articles_list, 'indexes':indexes})

def signupuser(request):
	if request.method == "GET":
		return render(request, 'stockapp/signupuser.html', {'form':CreateUserForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				if User.objects.filter(email=request.POST['email']).exists():
					return render(request, 'stockapp/signupuser.html', {'form':CreateUserForm(), 'error':'Email provided is already associated with an account.'})
				else:
					user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password1']) 
					user.save()
					login(request, user)
					messages.success(request, "User created successfully")
					return redirect('myportfolios')
			except IntegrityError: 
				return render(request, 'stockapp/signupuser.html', {'form':CreateUserForm(), 'error':'Username has already been taken.'})
		else:
			return render(request, 'stockapp/signupuser.html', {'form':CreateUserForm(), 'error':'Passwords did not match.'})

def loginuser(request):
	if request.method == "GET":
		return render(request, 'stockapp/loginuser.html', {'form':AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
		if user is None:
			return render(request, 'stockapp/loginuser.html', {'form':AuthenticationForm(), 'error':"Username and password did not match."})
		else:
			login(request, user)
			return redirect('myportfolios')

def logoutuser(request):
	if request.method == "POST":
		logout(request)
		return redirect('home')

def createportfolio(request):
	if request.method == "GET":
		ticker = request.GET.get('stock_ticker')
		if ticker != '' and ticker is not None:
			return redirect('stockpage', ticker)
		return render(request, 'stockapp/createportfolio.html', {'form':CreatePortfolioForm()})
	else:
		try:
			form = CreatePortfolioForm(request.POST)
			form.value = [Decimal(form['value'].value()[0]),'USD']
			newportfolio = form.save(commit=False)
			newportfolio.cash = newportfolio.value
			newportfolio.user = request.user
			newportfolio.portfolio_return = 0
			newportfolio.save()
			return redirect('home')
		except ValueError:
			return render(request, 'stockapp/createportfolio.html', {'form':CreatePortfolioForm(), 'error': 'Bad data passed in, try again.'})

def myportfolios(request):
	portfolios = Portfolio.objects.filter(user=request.user)
	ticker = request.GET.get('stock_ticker')
	if ticker != '' and ticker is not None:
		return redirect('stockpage', ticker)
	return render(request, 'stockapp/myportfolios.html', {'portfolios':portfolios})

def editportfolio(request, portfolio_pk):
	portfolio = get_object_or_404(Portfolio, pk=portfolio_pk, user=request.user)
	if request.method == "GET":
		form = EditPortfolioForm(instance=portfolio)
		return render(request, 'stockapp/editportfolio.html', {'portfolio':portfolio, 'form':form})
	else:
		try:
			form = EditPortfolioForm(request.POST, instance=portfolio)
			form.save()
			return redirect('myportfolios')
		except ValueError:
			return render(request, 'stockapp/editportfolio.html', {'portfolio':portfolio, 'form':form,'error': 'Bad data passed in, try again.'})

def deleteportfolio(request, portfolio_pk):
	portfolio = get_object_or_404(Portfolio, pk=portfolio_pk, user=request.user)
	if request.method == "POST":
		portfolio.delete()
		return redirect('myportfolios')


import yfinance as yf

def viewportfolio(request, portfolio_pk):
	portfolio_owner = Portfolio.objects.get(pk=portfolio_pk).user
	print(portfolio_owner)
	if request.method == "GET":
		ticker = request.GET.get('stock_ticker')
		if ticker != '' and ticker is not None:
			return redirect('stockpage', ticker)
		if Holding.objects.filter(portfolio=portfolio_pk):
			portfolio = list(Portfolio.objects.filter(id=portfolio_pk).values())
			qs = Holding.objects.filter(portfolio=portfolio_pk).order_by('ticker').values()
			list_qs = list(qs)
			tickers = list(qs.values('ticker'))
			l = [d['ticker'] for d in tickers]
			num = 0
			portfolio_value = []
			for ticker in l:
				d = list_qs[num]
				i = yf.Ticker(ticker)
				ask = i.info['ask']
				portfolio_value.append(d.get('shares')*ask)
				d['currentprice'] = ask
				d['return'] = ((d['currentprice']-float(d['avg_price']))/float(d['avg_price']))*100
				list_qs[num] = d
				num += 1
			portfolio_value.append(float(Portfolio.objects.values_list('cash', flat=True).get(id=portfolio_pk)))
			portfolio[0]['current_value'] = sum(portfolio_value)
			portfolio[0]['return'] = ((portfolio[0]['current_value']-float(portfolio[0]['value']))/float(portfolio[0]['value']))*100
			portfolio_object = Portfolio.objects.filter(id=portfolio_pk)
			portfolio_object.update(portfolio_return=portfolio[0]['return'])
			return render(request, 'stockapp/viewportfolio.html', {'portfolio':portfolio, 'holdings':list_qs, 'owner':portfolio_owner, 'form':SellForm()})
		else:
			ticker = request.GET.get('stock_ticker')
			if ticker != '' and ticker is not None:
				return redirect('stockpage', ticker)
			portfolio = list(Portfolio.objects.filter(id=portfolio_pk).values())
			portfolio[0]['return'] = ((float(portfolio[0]['cash'])-float(portfolio[0]['value']))/float(portfolio[0]['value']))*100
			portfolio_object = Portfolio.objects.filter(id=portfolio_pk)
			portfolio_object.update(portfolio_return=portfolio[0]['return'])
			return render(request, 'stockapp/viewportfolio.html', {'portfolio':portfolio})
	else:
		form = SellForm(request.POST)
		stock = yf.Ticker(form['ticker'].value())
		info = stock.info
		price = info['ask']
		transaction_value = int(form['shares'].value())*price
		holding = Holding.objects.filter(portfolio=portfolio_pk, ticker=form['ticker'].value())
		current_shares = holding.values_list('shares', flat=True)[0]
		shares_sold = int(form['shares'].value())
		portfolio = Portfolio.objects.filter(id=portfolio_pk)
		portfolio_cash = int(portfolio.values_list('cash', flat=True)[0])
		if current_shares-shares_sold == 0:
			portfolio.update(cash=portfolio_cash+transaction_value)
			holding.delete()
		else:
			portfolio.update(cash=portfolio_cash+transaction_value)
			holding.update(shares=current_shares-shares_sold)
		messages.success(request, "Sale processed successfully")
		return redirect('viewportfolio', portfolio_pk)

def stockpage(request, stock_ticker):
	ticker = request.GET.get('stock_ticker')
	if ticker != '' and ticker is not None:
		return redirect('stockpage', ticker)
	#Load stock page - get specific portfolios for buy form, pull stock info/historical data from yahoo finance
	try: 
		if request.user.is_authenticated:
			if request.method == "GET":
				#User's portfolios for buy form
				portfolios = Portfolio.objects.filter(user=request.user)
				#Yahoo Finance info for stock
				stock = yf.Ticker(stock_ticker)
				info = stock.info
				#Historical Data for Chart
				df = stock.history(period="1y", interval="1wk").dropna()
				labels = [x[:-9] for x in list(map(str, df.index.tolist()))]
				print(labels)
				data = [round(num, 2) for num in df['Close'].tolist()]
				print(data)
				return render(request, 'stockapp/stockpage.html', {'info':info, 'labels':labels,'data':data, 'portfolios':portfolios, 'form':BuyForm()})
			else:
				try:
					stock = yf.Ticker(stock_ticker)
					info = stock.info
					price = info['ask']
					ticker = info['symbol']
					name = info['shortName']
					form = BuyForm(request.POST)
					transaction_portfolio_cash = float(Portfolio.objects.filter(pk=form['portfolio'].value()).values_list('cash', flat=True)[0])
					transaction_value = int(form['shares'].value())*price

					#If there is not enough funds in the portfolio to perform transaction - reload stock page with error
					if transaction_portfolio_cash - transaction_value < 0:
						portfolios = Portfolio.objects.filter(user=request.user)
						stock = yf.Ticker(stock_ticker)
						info = stock.info
						df = stock.history(period="1y", interval="1wk").dropna()
						labels = [x[:-9] for x in list(map(str, df.index.tolist()))]
						data = [round(num, 2) for num in df['Close'].tolist()]
						return render(request, 'stockapp/stockpage.html', {'info':info, 'labels':labels,'data':data, 'portfolios':portfolios, 'form':BuyForm(), 'error': 'Insufficient funds within portfolio'})

					#If there is enough funds in the portfolio to perfom transaction check whether portfolio already owns that stock
					else:
						#If they do own that stock, update portfolio's cash, holding's number of shares and average price
						if Holding.objects.filter(portfolio=form['portfolio'].value(), ticker=ticker):
							remaining_value = transaction_portfolio_cash - transaction_value
							portfolio = Portfolio.objects.filter(pk=form['portfolio'].value())
							portfolio.update(cash=remaining_value)
							holding = Holding.objects.filter(portfolio=form['portfolio'].value(), ticker=ticker)
							avg_price = holding.values_list('avg_price', flat=True)[0]
							shares = holding.values_list('shares', flat=True)[0]
							holding.update(avg_price=(transaction_value+(float(shares*avg_price)))/(shares+int(form['shares'].value())))
							holding.update(shares=shares+int(form['shares'].value()))
							return redirect('myportfolios')

						#If they do not already own that stock, update portfolio's cash, and finish creating new holding object with ticker, name, avg_price and save
						else:
							remaining_value = transaction_portfolio_cash - transaction_value
							portfolio = Portfolio.objects.filter(pk=form['portfolio'].value())
							portfolio.update(cash=remaining_value)
							newholding = form.save(commit=False)
							newholding.ticker = ticker
							newholding.name = name
							newholding.avg_price = price
							newholding.save()
							return redirect('myportfolios')
				except ValueError:
					portfolios = Portfolio.objects.filter(user=request.user)
					stock = yf.Ticker(stock_ticker)
					info = stock.info
					df = stock.history(period="1y", interval="1wk").dropna()
					labels = [x[:-9] for x in list(map(str, df.index.tolist()))]
					data = [round(num, 2) for num in df['Close'].tolist()]
					return render(request, 'stockapp/stockpage.html', {'info':info, 'labels':labels,'data':data, 'portfolios':portfolios, 'form':BuyForm(), 'error': 'Bad data passed in, try again.'})
		else:
			#Yahoo Finance info for stock
			stock = yf.Ticker(stock_ticker)
			info = stock.info
			#Historical Data for Chart
			df = stock.history(period="1y", interval="1wk").dropna()
			labels = [x[:-9] for x in list(map(str, df.index.tolist()))]
			data = [round(num, 2) for num in df['Close'].tolist()]
			return render(request, 'stockapp/stockpage.html', {'info':info, 'labels':labels,'data':data})
	except (ValueError, KeyError, TypeError) as e:
		messages.error(request, "Stock ticker not found")
		return redirect('home')

def powerbitest(request):
	return render(request, 'stockapp/powerbitest.html')


def hannah(request):
	tickers = ["AXP","AMGN","AAPL","BA","CAT","CSCO","CVX","GS","HD","HON","IBM","INTC","JNJ","KO","JPM","MCD","MMM","MRK","MSFT","NKE","PG","UNH","CRM","VZ","V","WBA","WMT","DIS","DOW"]
	stocks = []
	ask = []
	for t in tickers:
		stocks.append(yf.Ticker(t).info['shortName'])
	print(stocks)
	return render(request, 'stockapp/hannah.html')