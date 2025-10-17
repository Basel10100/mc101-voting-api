poetry-update: 
	poetry update

poetry-export:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from test_runner
	docker compose -f docker-compose.test.yml down -v

backup-now:
	docker compose run --rm db_backup_cron /usr/local/bin/backup.sh