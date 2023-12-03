# build application
sudo docker-compose up --build

# run server
sudo docker-compose up

# run commands on docker 
sudo docker-compose exec web python manage.py makemigrations
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py shell