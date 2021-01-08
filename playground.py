import datetime
today = datetime.datetime.now().strftime("%d/%m/%Y")
six_month = datetime.datetime.now().today() + datetime.timedelta(6 * 30)
six_month = six_month.strftime("%d/%m/%Y")
print(today)
print(six_month)
