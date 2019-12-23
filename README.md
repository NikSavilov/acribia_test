# URL Checker

### Installation:

```
sudo -s
git clone https://github.com/NikSavilov/acribia_test.git
cd acribia_test
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 manage.py migrate
```

To run celery:
```
celery worker -A acribia_test &
```

To run development server:
```
python3 manage.py runserver
```

RabbitMQ required, change credentials in settings.py.

![Screenshot](https://raw.githubusercontent.com/NikSavilov/acribia_test/master/Screenshot.jpg)
