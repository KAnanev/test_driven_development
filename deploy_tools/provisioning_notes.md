Обеспечение работы нового сайта
================================
## Необходимые пакеты:
* nginx
* Python 3.8
* virtualenv + pip
* Git
* Gunicorn
## Конфигурация виртуального узла Nginx
* см. nginx.template.conf
## Служба Systemd
* см. gunicorn-systemd.template.service
* см. gunicorn-systemd.template.socket
## Структура папок:
Если допустить, что есть учетная запись пользователя в /home/username
/home/username
    └── sites
        └── SITENAME
            ├── database
            ├── source
            ├── static
            └── virtualenv
