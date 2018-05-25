run:
	flask run

debug:
	export FLASK_DEBUG=1

start_db:
	sudo service postgresql start
