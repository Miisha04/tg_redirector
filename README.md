# tg_redirector
You can use your own redirector in Telegram

How to use it?

1) **Clone the repository**
You can use git clone or just download the files

2) **Create venv and install dependencies**

Command to create venv:
```python -m venv venv```    (second parameter is name of your vurtual environment)

Command to activate venv:
```venv\Scripts\activate```

Command to install dependencies:
```pip install -r requirements.txt```

3) **Run python script**

You can write command:
```python redirector.py```
Or just use run button if you set up the interpreter in your IDE

4) **Enter ID and HASH in Telegram API:**
   
When you run script, you need to enter ID and HASH. To get this data we need to log in in telegram API [URL](https://my.telegram.org/auth) and check your endpoint, you can see there _?to=deactivate_, you need to delete, It must be only https://my.telegram.org/auth

There you can log in your telegram account (you`d better to use your fake profile)
Then click _API development tools_ and create your app, then you will see data of your app - ID, HASH and other

When you enter your ID, HASH, phone number in script, you need to enter confirmation code in telegram and data will be saved in file credentials.txt and you wont have to enter these parameters one more time

If you get error check credentials.txt, you need to have 3 rows id, hash, phone number. Also, you can write it down in this file. 

5) **Enter source ID and destination ID**
   
You can use tg bot - _@username_to_id_bot_ to get ID
After that your script will redirect messages from source to destination while script works, **but you need to have source and destination in your chat list.**

-------------------------
**IF YOU WANT TO SUPPORT ME:**

>Phantom: 72n9LgeXzYoABxxbsZ2JQuF5d9PB561jJXwpQjevPmBH

>Metamask: 0x709Cc64e2D4DE967B425785d5D355FF55541B082




