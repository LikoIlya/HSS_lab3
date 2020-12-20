# Lab 3 (Mongo)

- docker-compose up -d
- sudo ./init_rs.sh
- (wait several seconds)
- docker-compose exec router1 sh -c “mongo < .scripts/init-router.js”
- run all generate_data.ipynb
- cp mongo_lab/rides.csv mongo_lab/data/
- sudo sh import_and_query_data.sh
- docker-compose down -v --rmi all --remove-orphans