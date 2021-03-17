import requests
from restaurant import restaurant_data
from users import user_data
user_url = 'http://127.0.0.1:8000/api/user'
restaurant_url = "http://127.0.0.1:8000/api/restaurants"

most_popular_url = "http://127.0.0.1:8000/api/most-popular"
transaction_url = "http://127.0.0.1:8000/api/transaction"
number_of_user_url = "http://127.0.0.1:8000/api/number-of-users"
top_x_user_url = "http://127.0.0.1:8000/api/top-x-user"


def CreatUser(name,cash_balance):
    response = requests.post(user_url, data={
        "name" : name,
        "cash_balance": cash_balance
    })
    return response

myobj = {'somekey': 'somevalue'}
NUMBER_OF_USER = 1000
NUMBER_OF_RESTAURANT = 100 
NUMBER_OF_FOOD_ITEM = 100
NUMBER_OF_TRANSACTION = 300

USER_NAMES = []
CASH_BALANCE = []
    

# for res in restaurant_data:
#     res


# for i in range(NUMBER_OF_USER):
#     CreatUser(user_data[i]['name'], float(user_data[i]['cashBalance']))

for i in range(NUMBER_OF_RESTAURANT):
    print(restaurant_data[i])
    res = restaurant_data[i] 
    res["cashBalance"]
    break
    # print (CreatUser(name,cash_balance))

    # for transaction in user["purchaseHistory"]:
    #     print (transaction)
# x = requests.post(user_url, data=myobj)
# print(x.text)


