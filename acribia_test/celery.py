import os
import threading
import time
import traceback
from queue import Queue
import requests
from asgiref.sync import async_to_sync
from celery import Celery
from channels.layers import get_channel_layer
from django.conf import settings
from list.list import paths

app = Celery('acribia_test', broker='amqp://guest:12345@localhost:5672//')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acribia_test.settings')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(ignore_result=True)
def check_url(url, key=""):
	def worker(q, cl, j):
		while not q.empty():
			url_ = q.get()
			try:
				r = requests.head(url_)
				redirected = False
				for r_ in r.history:
					if 300 <= r_.status_code < 309:
						redirected = True
				async_to_sync(cl.group_send)(
					key,
					{
						"type": "channel_message",
						'url': url_,
						'exists': "✅ - 200" if r.status_code == 200 else "⤴ - 3**" if redirected else "⛔ - 4**" + str(time.time())
					}
				)
			except:
				pass
			q.task_done()
		return True

	try:
		channel_layer = get_channel_layer()
		queue = Queue()
		for i, path in enumerate(paths[:300]):
			new_url = url + path + '/'
			queue.put(new_url)
		workers = []
		for i in range(50):
			t = threading.Thread(target=worker, args=(queue, channel_layer, i), daemon=True)
			t.start()
		for w in workers:
			w.join()
		return "Done"
	except:
		return traceback.format_exc()