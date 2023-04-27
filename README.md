## AO3 Web Reader

Reimplementation of [ao3-web-reader](https://github.com/zNitche/ao3-web-reader). 
This project won't be updated along with `ao3-web-reader`.

---

### Technologies
- Django 4.2
- gunicorn
- nginx
- redis
- bootstrap
- celery

### Features
- Accounts authentication.
- Getting works from ao3.
- Grouping works using tags.
- Auto-update of added works.
- Downloading works.

### Setup
#### Dev
1. Generate `.env` config file
```
python3 generate_dotenv.py
```
2. Run dev docker container.
```
sudo docker compose -f docker-compose-dev.yml up
```
#### Prod
to do...