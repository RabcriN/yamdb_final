import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    DATA = {
        User: "users.csv",
        Category: "category.csv",
        Genre: "genre.csv",
        Title: "titles.csv",
        Review: "review.csv",
        Comment: "comments.csv",
        Title.genre.through: "genre_title.csv",
    }

    def add_arguments(self, parser):
        parser.add_argument("--data_directory", type=str)

    def handle(self, *args, **options):
        dirname = options["data_directory"] or "static/data/"
        for model, filename in self.DATA.items():
            with open(
                f"{dirname}/{filename}",
                newline="",
                encoding="utf-8"
            ) as csvfile:
                reader = csv.DictReader(csvfile, delimiter=",")
                for row in reader:
                    model.objects.update_or_create(id=row["id"], defaults=row)
            print(f"{filename} successfully added to DB")
        print("DB successfully filled")
