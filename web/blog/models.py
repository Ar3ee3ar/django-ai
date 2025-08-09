from django.db import models
# ---- note ------------------
# need to migrate database because from code the database is still not real
# and don't working so we need to do "Migrations" and "Migrate"
# 1. Migrations: update database to match current status
# --> python manage.py makemigrations
# 2. Migrate: send database to update real database
# --> python manage.py migrate
# -----------------------------
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    date_created =models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.title