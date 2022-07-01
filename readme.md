#### Setup & Guide

At first install all the packages by typing
`pip install requirements.txt`

Then run the project by typing
`python manage.py runserver`

#### The endpoints
- To see user list/all user data -> <http://127.0.0.1:8000/authentication/user-list/>
- To create a new user -> <http://127.0.0.1:8000/authentication/user-list/>
- To view a particular user detail -> <http://127.0.0.1:8000/authentication/user-detail/uid/>
> uid refers to a user's uid
- To see transaction history list -> <http://127.0.0.1:8000/transaction/transaction-history-list/>
- To view a particular user transaction history list -> <http://127.0.0.1:8000/transaction/transaction-history-detail/mobile_number/>
> mobile_number refers to a user's mobile number
- To make a transaction -> <http://127.0.0.1:8000/transaction/transaction-history-list/>

### Note
#### Using postman
- To create a new user, use post method and pass data as json format to the endpoint <http://127.0.0.1:8000/authentication/user-list/>
`
{
    "username": "Test User 100",
    "mobile_number": "00001"
}
`
- To make a transaction, use post method and pass data as json format to the endpoint <http://127.0.0.1:8000/transaction/transaction-history-list/>

`
{
    "user": {
        "username": "admin",
        "mobile_number": "1234"
    },
    "transaction": [
        {
            "sent_amount": "20.00",
            "transfer_scheduled_time": "2022-01-30T21:40:34",
            "receiver": {
                "username": "John",
                "mobile_number": "90871245"
            }
        },
        {
            "sent_amount": "10.00",
            "receiver": {
                "username": "Dummy User",
                "mobile_number": "012485349"
            }
        },
        {
            "sent_amount": "50.00",
            "transfer_scheduled_time": "2022-01-30T23:46:34",
            "receiver": {
                "username": "Samin",
                "mobile_number": "4567"
            }
        }
    ]
}
`