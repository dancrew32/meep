make:
	vim makefile

checkin:
	git add -A && git commit && git push origin main

venv:
	virtualenv -p python3 venv

deps:
	./venv/bin/pip3 install -r requirements.txt

serve:
	./venv/bin/python3 serve.py
