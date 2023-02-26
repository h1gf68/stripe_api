# stripe_api

Скопируйте проект
<pre>git clone https://github.com/h1gf68/stripe_api.git</pre>

Перейдите в папку проекта
<pre>cd stripe_api</pre>

Запустите виртуальное окружение
<pre>python3 -m venv myvenv</pre>

Активируйте виртуальное окружение
<pre>source myvenv/bin/activate</pre>

Установите зависимости
<pre>pip install -r requirements.txt</pre>

Проведите миграции базы данных
<pre>python manage.py migrate</pre>
<pre>python manage.py makemigrations</pre>
<pre>python manage.py migrate</pre>


Измените значения ключей в файле .env:

Секретный ключ django например
<blockquote>SECRET_KEY="django-insecure-@7getf0x=opao)&=l)cw(@7@*5ryxjzp#o2osvh=r4$!gw0s#t"</blockquote>

Публичный и секретный ключи stripe. Доступны после регистрации по адресу https://dashboard.stripe.com/test/apikeys
<blockquote>
STRIPE_PUBLIC_KEY=<YOUR_STRIPE_PUBLIC_KEY><br/>
STRIPE_SECRET_KEY=<YOUR_STRIPE_SECRET_KEY>
</blockquote>

Ключ STRIPE_ENDPOINT_SECRET необходим для подтвержения платежа.<br/>
Чтобы получить этот ключ перейдите https://stripe.com/docs/stripe-cli и повторите команды в зависимости от вашей операционной системы. 

Затем в новом окне терминала запустите stripe на прослушивание (https://dashboard.stripe.com/test/webhooks/create?endpoint_location=local)
<pre>./stripe listen --forward-to localhost:8080/webhook</pre>
В терминале отобразится ключ (например whsec_683...7a13ff), его нужно записать вместо <YOUR_STRIPE_ENDPOINT_SECRET>
STRIPE_ENDPOINT_SECRET=<YOUR_STRIPE_ENDPOINT_SECRET>

Создайте  root-пользователя
<pre>python manage.py createsuperuser</pre>

Запустите сервер
<pre>python manage.py runserver</pre>

Перейдите http://127.0.0.1:8000/admin/
и добавьте несколько Items

Затем перейдите на http://127.0.0.1:8000 и сделать заказ
при оплате используйте тестовый номер карты от stripe(4242 4242 4242 4242)
