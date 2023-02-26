# stripe_api

Скопируйте проект
<pre>git clone https://github.com/h1gf68/stripe_api.git</pre>

Перейдите в папку проекта
cd stripe_api

Запустите виртуальное окружение
python3 -m venv myvenv

Активируйте виртуальное окружение
source myvenv/bin/activate

Установите зависимости
pip install -r requirements.txt

Проведите миграции базы данных
python manage.py migrate
python manage.py makemigrations
python manage.py migrate


Измените значения ключей в файле .env:

Секретный ключ django например 
SECRET_KEY="django-insecure-@7getf0x=opao)&=l)cw(@7@*5ryxjzp#o2osvh=r4$!gw0s#t"

Публичный и секретный ключи stripe. Доступны после регистрации по адресу https://dashboard.stripe.com/test/apikeys

STRIPE_PUBLIC_KEY=<YOUR_STRIPE_PUBLIC_KEY> 
STRIPE_SECRET_KEY=<YOUR_STRIPE_SECRET_KEY>

Ключ STRIPE_ENDPOINT_SECRET необходим для подтвержения платежа.
Чтобы получить этот ключ перейдите https://stripe.com/docs/stripe-cli и повторите команды в зависимости от вашей операционной системы. 

Затем в новом окне терминала запустите stripe на прослушивание (https://dashboard.stripe.com/test/webhooks/create?endpoint_location=local)
./stripe listen --forward-to localhost:8080/webhook
В терминале отобразится ключ (например whsec_683...7a13ff), его нужно записать вместо <YOUR_STRIPE_ENDPOINT_SECRET>
STRIPE_ENDPOINT_SECRET=<YOUR_STRIPE_ENDPOINT_SECRET>

Создайте  root-пользователя
python manage.py createsuperuser

Запустите сервер
python manage.py runserver

http://127.0.0.1:8000/admin/
Добавить несколько Items

Затем перейдите на http://127.0.0.1:8000 и сделать заказ
при оплате используйте тестовый номер карты от stripe(4242 4242 4242 4242)