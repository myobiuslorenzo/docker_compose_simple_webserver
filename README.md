**Данный проект реализует веб-сервер из трех сервисов с помощью docker-compose и Dockerfile.** \
* Код писался и тестировался на локальной машине, в initial.sh действия, которые необходимы для работы\
* проекта(установка docker, docker-compose, создание venv..), файл может быть важен в случае больших трудностей \
* с тестированием на другой машине. \

Сервис 1 -- база данных (запускается первым) \
Сервис 2 -- скрипт для заполнения базы данных (запускается после сервиса 1) \
Сервис 3 -- веб-сервер, возвращающий данные из бд сервиса 1 по http-запросу (запускается после сервиса 1) \
Сервисы общаются внутри одной docker-сети. \
Сервис 3 имеет проброшенный порт 8000:8000 \
К сервису 1 подключение осуществляется по порту 3306 \
Сервис 2 добавляет данные при запуске и при каждом обновлении html-страницы. \
Данные сервиса 1 не теряются при удалении контейнера (см. volumes). \

Для сервиса базы данных используется готовый образ mysql. \
На сервере БД создается база данных mysql_database с таблицей 
users, которая хранит столбцы name и age с помощью скрипта /sql_init/init.sql \

Код сервиса 2 лежит в папке filler, код для сервиса 3 в папке webservice \
Сервис 2 выводит содержимое базы данных после ее заполнения в логи (их видно при запуске команды docker-compose up). \
Это нужно для проверки того, что бд заполняется данными корректно. \
Данные для заполнения берутся из файла data.csv \

Проверить работоспособность сервисов 2 и 3 можно пройдя по ссылкам из логов, т.е. вбить в строку браузера \
нечто в духе(адреса каждый раз новые) http://172.19.0.4:5000 для сервиса 2 \
или http://172.19.0.4:8000/health для сервиса 3. \
Либо отправить http-запрос через curl http://172.19.0.4:5000 \
Страница health для сервера 3 есть проверка его работоспособности, \
возвращает JSON {"status": "OK"}, стат. 200 \
Подключиться к БД и посмотреть ее руками можно с помощью комманд: \
<code>'''
docker exec -it shpuntenkool-hwdocker_db_1  mysql -uroot -p
docker exec -it shpuntenkool-hwdocker_db_1  mysql sh
'''
</code>
В первом варианте можно писать sql-запросы, во втором подключение к linux-терминалу. \

**ПРО СЕТИ**
Для создания macvlan-сети я пыталась использовать скрипт net.sh \
Этот скрипт динамически ищет нужные параметры (subnet, gateway, parent), что при удачном стечении обстоятельств \
должно избавить от хардкода + на другой машине будут иные значения этих параметров. \
Однако мой роутер не позволяет использовать promiscuous mode и команда ip link set "$PFACE" promisc on \
не работает.\
"$PFACE" -- имя wi-fi сети.
Возможно я не совсем понимаю что от меня требуется и нужно запускать скрипты сервисов 2-3 не через \
браузер или curl. \
Так или иначе, используя macvlan, я не могу связаться хостом с контейнерами и наоборот.\
При этом контейнеры к этой сети успешно подключаются как к external network. \
В итоге я решила пока отказаться от macvlan и оставить создаваемую по умолчанию сеть.\
Поэтому чтобы посмотреть на работу с macvlan надо раскомментировать все строки в docker-compose.yml \
(возможно на сервере проблем не будет :с) \
(p.s. для этого необходимо запустить net.sh перед подниманием контейнеров !!)
В стандартной сети проблем нет и все работает нормально. \
Запускать с помощью последовательных команд: \
<code>'''
docker-compose build 
docker-compose up 
'''
</code>
В последней команде -d скроет логи. \