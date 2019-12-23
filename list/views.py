import json

from django.http import Http404
from django.shortcuts import render
from django.utils.safestring import mark_safe
from list.list import paths
from acribia_test.celery import check_url


def index(request):
	try:
		url = request.GET["url"]
	except:
		url = None
	if url:
		if not request.session.exists(request.session.session_key):
			request.session.create()
		session_key = request.session.session_key

		task = check_url.delay(url, session_key)
		return render(request, 'list/index.html', {
			'url_json': mark_safe(json.dumps(url)),
			"key": session_key
		})
	raise Http404
