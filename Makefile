try:
	sudo docker compose exec web bash -c "python3 manage.py shell < try.py"
load:
	sudo docker compose exec web python3 manage.py loaddata data.json
super:
	sudo docker compose exec web python3 manage.py createsuperuser
mg:
	sudo docker compose exec web python3 manage.py makemigrations
	sudo docker compose exec web python3 manage.py migrate
generate:
	sudo docker compose exec web python3 manage.py generate