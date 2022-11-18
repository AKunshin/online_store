# Задание:
-------

* Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
* Django Модель `Item` с полями `(name, description, price) `
* API с двумя методами:
    * GET `/buy/{id}`, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполненииэтого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос` stripe.checkout.Session.create(...)` и полученный session.id выдаваться в результате запроса
    * GET `/item/{id}`, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном `Item` и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на `/buy/{id}`, получение session_id и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму `stripe.redirectToCheckout(sessionId=session_id)`

* Залить решение на Github, описать запуск в README.md

* Запуск используя `Docker`

* Просмотр Django Моделей в Django Admin панели - доступно по адресу `127.0.0.1:8000/admin`

* Главная страница: `127.0.0.1:8000`

Если в dashboard.stripe у вас был заведен товар, он автоматически создастся в БД

API метод для получения HTML c кнопкой на платежную форму от Stripe для Item с id=1:
```
curl -X GET http://localhost:8000/item/1
```
Результат - HTML c инфой и кнопкой:
```
<html>
  <head>
    <title>Buy Item 1</title>
  </head>
  <body>
    <h1>Item 1</h1>
    <p>Description of Item 1</p>
    <p>1111</p>
    <button id="buy-button">Buy</button>
    <script type="text/javascript">
      var stripe = Stripe('pk_test_a9nwZVa5O7b0xz3lxl318KSU00x1L9ZWsF');
      var buyButton = document.getElementById(buy-button');
      buyButton.addEventListener('click', function() {
        // Create a new Checkout Session using the server-side endpoint 
        // Redirect to Stripe Session Checkout
        fetch('/buy/1', {method: 'GET'})
        .then(response => return response.json())
        .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
      });
    </script>
  </body>
</html>
```


# Запуск
------
```
git clone https://github.com/AKunshin/online_store.git
cd online_store
python3 -m venv env
```
Для Linux:
```
. ./env/bin/activate
```

Для Windows:
```
.\env\Scripts\activate
```
Необходимо создать файл .env и заполнить его своими данными, по образцу .env_example:

```
SECRET_KEY = 'your_secret_key_for_django_settings'
STRIPE_SECRET_KEY = 'sk_test_'
STRIPE_PUBLISHABLE_KEY = 'pk_test_'
```

Далее снова в консоли:
```
pip install -r requirements.txt
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### Создание учетной записи администратора
```
python manage.py createsuperuser
```

# Запуск Docker
------
```
docker-compose build
docker-compose up -d
```
##### Остановка docker:
-------
```
docker-compose stop
```
Перейти на главную страницу:
```
http://localhost:8000/
```
Если в dashboard.stripe у вас был заведен товар, он автоматически создастся в БД
