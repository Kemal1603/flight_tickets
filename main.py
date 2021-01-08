# ---------------------------- IMPORTED MODULES ------------------------------- #
import requests
import datetime

# ---------------------------- CONSTANTS------------------------------- #
FLY_FROM_IATA_CODE = "MSQ"
# ---------------------------- SHEET API ------------------------------- #
sheet_api_url = "https://api.sheety.co/c1941eafc77ece7d14cdfcb3121fd0c9/flightDeals/prices"
response_from_sheet = requests.get(url=sheet_api_url)
cities_details = response_from_sheet.json()["prices"]
iata_codes = ''
for el in cities_details:
	iata_codes += f'{el["iataCode"]},'
print(iata_codes[:-1])
# ---------------------------- KIWI FLIGHT TICKETS API ------------------------------- #
today = datetime.datetime.now().strftime("%d/%m/%Y")
six_month = datetime.datetime.now().today() + datetime.timedelta(6 * 30)
six_month = six_month.strftime("%d/%m/%Y")
tickets_search_api_header = {
	"apikey": "_dlEv4_CHzrPQpacYiuWQmw4UpZGYY4A"
}

tickets_search_api_respond = requests.get(url=f"https://tequila-api.kiwi.com/v2/search?"
                                              f"fly_from={FLY_FROM_IATA_CODE}&fly_to={iata_codes[:-1]}"
                                              f"&dateFrom={today}&dateTo={six_month}&"
                                              f"one_for_city=1&curr=USD",
                                          headers=tickets_search_api_header)


flights_details = tickets_search_api_respond.json()["data"]
output_data = []
cheapest_cities = {}
for el in flights_details:
	flight_date = el['local_arrival'].split('T')[0]

	if el['cityTo'] not in output_data:
		output_data.append({
			'city': el['cityTo'],
			'lowestPrice': f"{el['price']}",
			'date': f"{datetime.date(int(flight_date[:4]), int(flight_date[5:7]), int(flight_date[8:10])).strftime('%d/%m/%Y')}"
		})


for new_data in output_data:
	city = new_data["city"]
	lowestPrice = int(new_data["lowestPrice"])
	for old_data in cities_details:
		if old_data["city"] == city:
			if lowestPrice < old_data["lowestPrice"]:
				cheapest_cities[city] = lowestPrice
print(cheapest_cities)
