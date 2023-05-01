import csv

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Categories, Comment, Genre, Review, Title, User

TABLES = {
    User: 'users.csv',
    Categories: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):
    """
    Импорт файлов csv в базу данных sqlite
    """

    def handle(self, *args, **kwargs):
        for model, csv_f in TABLES.items():
            with open(
                    f'{settings.BASE_DIR}/static/data/{csv_f}',
                    'r',
                    encoding='utf-8'
            ) as csv_file:
                if model == Title:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        category_obj, created = Title.objects.get_or_create(
                            category_id=row['category'],
                            name=row['name'],
                            year=row['year'],
                            description=None,
                        )
                if model == Review:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        category_obj, created = Review.objects.get_or_create(
                            title_id=row['title_id'],
                            text=row['text'],
                            author_id=row['author'],
                            score=row['score'],
                            pub_date=row['pub_date'],
                        )
                if model == Comment:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        category_obj, created = Comment.objects.get_or_create(
                            review_id=row['review_id'],
                            text=row['text'],
                            author_id=row['author'],
                            pub_date=row['pub_date'],
                        )

                else:
                    reader = csv.DictReader(csv_file)
                    model.objects.bulk_create(
                        model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
