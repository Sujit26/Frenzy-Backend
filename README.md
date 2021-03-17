# Frenzy-Backend

OPERATION REQUINMENTS

## 1.  List all restaurants that are open at a certain datetime  
    API CALL => get http://127.0.0.1:8000/api/restaurants?time=1615841024 

    time: integar value(time in epoch format)

```json 
output :
[
    {
        "cash_balance": 1000.0,
        "name": "Tummy",
        "menu": [
            {
                "name": "Pizza",
                "price": 100.0
            }
        ],
        "opening_time": [
            {
                "weekday": 2,
                "from_hour": "01:26:14",
                "to_hour": "19:26:29"
            },
            {
                "weekday": 1,
                "from_hour": "10:26:49",
                "to_hour": "19:26:50"
            }
        ]
    }
] 
```

-------------------------------------------------------------------------------------------------
## 2.  List all restaurants that are open for more or less than x hours per day or week
    API CALL => get http://127.0.0.1:8000/api/restaurants?time=1615841024

```json
Response: 
    {
        "cash_balance": 1021.0,
        "name": "Domino'z",
        "menu": [
            {
                "name": "Pizza 1",
                "price": 120.0
            },
            {
                "name": "HamBurger",
                "price": 2000.0
            }
        ],
        "opening_time": [
            {
                "weekday": 0,
                "from_hour": "00:07:44",
                "to_hour": "14:07:45"
            }
        ]
    }
```

-------------------------------------------------------------------------------------------------
## 3.  List all restaurants that have more or less than x number of dishes within a price range
    API CALL => get http://127.0.0.1:8000/api/restaurants?min_price=12&mode=gte&nod=1

        nod:        number of dishes
        min_price:  minimum price
        max_price:  maximum price
        mode: 
                    gte [for greater than & equal to]
                    lte [for less then & equal to]
    Assumptions 
    - by default we are taking min_price = 0 & max_price = 999999
    - nod=1 is nessary otherwise it will return all restaurants

```json
Output:
[
    {
        "cash_balance": 1000.0,
        "name": "Tummy",
        "menu": [
            {
                "name": "Pizza",
                "price": 100.0
            }
        ],
        "opening_time": [
            {
                "weekday": 2,
                "from_hour": "01:26:14",
                "to_hour": "19:26:29"
            },
            {
                "weekday": 1,
                "from_hour": "10:26:49",
                "to_hour": "19:26:50"
            }
        ]
    },
    {
        "cash_balance": 1000.0,
        "name": "Yummy",
        "menu": [
            {
                "name": "Burger",
                "price": 11.0
            }
        ],
        "opening_time": []
    }
]
```
-------------------------------------------------------------------------------------------------
## 4.  Search for restaurants or dishes by name, ranked by relevance to search term
    API CALL => get http://127.0.0.1:8000/api/restaurants?name=yumm  
    name:   name of restaurant 

    return list of restaurants after full text search on resutaurant names
```json
Response: 
[
    {
        "cash_balance": 1000.0,
        "name": "Yummy",
        "menu": [
            {
                "name": "Burger",
                "price": 11.0
            }
        ],
        "opening_time": []
    }
]
```
    
    
-------------------------------------------------------------------------------------------------
## 5.  The top x users by total transaction amount within a date range
    API CALL => get http://localhost:8000/api/top-x-user?min_date=1615841024&max_date=1615841024&value=10
    
        min_date: starting date of search in epoch (by default it will take date & time for current day)
        max_date: ending date of search in epoch   (by default it will take date & time for current day)
        value:    number of dollars
        mode:     'lte' or 'gte'
                    - lte: less then or equal to
                    - gte: greater then or equal to 
```json
Response: 
[
    {
        "cash_balance": 1000.0,
        "id": 2,
        "name": "Sidhant Jain",
        "purchase_history": [
            {
                "id": 1,
                "transaction_amount": 12.0,
                "transaction_date": "2021-03-16T20:00:04Z",
                "user": 2,
                "dish_name": 1,
                "restaurant": 2
            },
            {
                "id": 3,
                "transaction_amount": 12.0,
                "transaction_date": "2021-03-16T20:04:32Z",
                "user": 2,
                "dish_name": 2,
                "restaurant": 2
            }
        ]
    }
]
```

-------------------------------------------------------------------------------------------------
## 6.  The most popular restaurants by transaction volume, either by number of transactions or transaction dollar value
    
    API CALL => http://127.0.0.1:8000/api/most-popular?max_amount=10&mode=gte&min_date=1615841024&max_date=1615841024
        
        max_amount: number of dollars
        min_date: starting date of search in epoch (by default it will take date & time for current day)
        max_date: ending date of search in epoch   (by default it will take date & time for current day)
        mode: 
                    'gte' [for greater than & equal to]
                    'lte' [for less then & equal to] 

```json
sample output:

{
    "Number of user": 10
}
```
-------------------------------------------------------------------------------------------------
## 7.  Total number of users who made transactions above or below $v within a date range  

    API CALL => http://127.0.0.1:8000/api/user?min_date=1615841024&max_date=1615841024&value=2&mode=lte  

        min_date: starting date of search in epoch (by default it will take date & time for current day)
        max_date: ending date of search in epoch    (by default it will take date & time for current day)
        value:    number of dollars
        mode:     'lte' or 'gte'
                    - lte: less then or equal to
                    - gte: greater then or equal to 

-------------------------------------------------------------------------------------------------
## 8.  Process a user purchasing a dish from a restaurant, handling all relevant data changes in an atomic transaction

    API CALL => get http://127.0.0.1:8000/api/transaction
```json
Response: List all the transactions
[
    {
        "id": 1,
        "transaction_amount": 12.0,
        "transaction_date": "2021-03-16T20:00:04Z",
        "user": 2,
        "dish_name": 1,
        "restaurant": 2
    },
    {
        "id": 2,
        "transaction_amount": 1.0,
        "transaction_date": "2021-03-16T20:01:32Z",
        "user": 1,
        "dish_name": 1,
        "restaurant": 1
    },
    {
        "id": 3,
        "transaction_amount": 12.0,
        "transaction_date": "2021-03-16T20:04:32Z",
        "user": 2,
        "dish_name": 2,
        "restaurant": 2
    },
    {
        "id": 4,
        "transaction_amount": 100.0,
        "transaction_date": "2021-03-17T13:47:59.022761Z",
        "user": 1,
        "dish_name": 1,
        "restaurant": 1
    }
]
```

    API CALL => post http://127.0.0.1:8000/api/transaction
    
    data: {
    "user": 1,
    "dish_name": 1
    }

```json
Response:
{
    "id": 4,
    "transaction_amount": 100.0,
    "transaction_date": "2021-03-17T13:47:59.022761Z",
    "user": 1,
    "dish_name": 1,
    "restaurant": 1
}
```


-------------------------------------------------------------------------------------------------
OPERATION REQUINMENTS
# Models
## Restaurant
- id
- name
- cash_balance

## FoodItem
- id
- name
- price
- restaurant

## OpenningTime
- weekday
- from_hour
- to_hour
- restaurant

## User
- name
- id
- cash_balance

## Transaction

- user_id (f_key to User)
- dish_name
- restaurant_name
- transaction_amount
- transaction_date


## WEEKDAYS 
[
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
]

--------------------------------------------------------------------------------------------------------------------------
Assumption

- If any restaurant opens more or less than X hours then we consider in Requinment number 2. It is not nesessary to open more or less then X hours daily.
- We create full text search for restaurant & dishes.
