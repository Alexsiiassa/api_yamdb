from csv import DictReader
from django.core.management import BaseCommand


from reviews.models import Category, Genre, Review
from reviews.models import Title, User, Comment, TitleGenre


ALREDY_LOADED_ERROR_MESSAGE = """
Если вам нужно перезагрузить дочерние данные из CSV-файла,
сначала удалите файл db.sqlite3, чтобы уничтожить базу данных.
Затем запустите `python manage.py миграция` для новой пустой
базы данных с таблицами"""


class User(BaseCommand):
    help = "Загружает данные из user.csv"

    def handle(self, *args, **options):
        if User.objects.exists():
            print('дочерние данные уже загружены... существующие.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        for row in DictReader(
            open('./static/data/user.csv')
        ):
            user = User(
                id=row['id'], username=row['username'],
                email=row['email'], role=row['role'],
                bio=row['bio'], first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()


class Command(BaseCommand):
    help = "Загружает данные из category.csv"

    def handle(self, *args, **options):
        if Category.objects.exists():
            print('дочерние данные уже загружены... существующие.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        for row in DictReader(
            open('./static/data/category.csv')
        ):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()


class Genre(BaseCommand):

    help = "Загружает данные из genre.csv"

    def handle(self, *args, **options):
        if Genre.objects.exists():
            print('дочерние данные уже загружены... существующие.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        for row in DictReader(
            open('./static/data/genre.csv')
        ):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()


class Review(BaseCommand):
    help = "Загружает данные из review.csv"

    def handle(self, *args, **options):
        if Review.objects.exists():
            print('дочерние данные уже загружены... существующие.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        for row in DictReader(
            open('./static/data/review.csv')
        ):
            review = Review(
                id=row['id'], title_id=row['title_id'],
                text=row['text'], author=row['author'],
                score=row['score'], pub_date=row['pub_date']
            )
            review.save()


class Command(BaseCommand):
    help = "Загружает данные из title.csv"

    def handle(self, *args, **options):
        if Title.objects.exists():
            print('дочерние данные уже загружены... существующие.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        for row in DictReader(
            open('./static/data/titles.csv')
        ):
            title = Title(
                id=row['id'], name=row['name'],
                year=row['year'], category_id=row['category']
            )
            title.save()


class Comment(BaseCommand):
    help = "Загружает данные из comment.csv"

    def handle(self, *args, **options):
        if Comment.objects.exists():
            print('дочерние данные уже загружены... существующие.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        for row in DictReader(
            open('./static/data/comment.csv')
        ):
            comment = Comment(
                id=row['id'], review_id=row['review_id'],
                text=row['text'], author=row['author'],
                pub_date=row['pub_date']
            )
            comment.save()


class Command(BaseCommand):
    help = "Загружает данные из genre_title.csv"

    def handle(self, *args, **options):
        if TitleGenre.objects.exists():
            print('дочерние данные уже загружены... существующие.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return

        print("Загрузка данных")

        for row in DictReader(
            open('./static/data/genre_title.csv')
        ):
            titlegenre = TitleGenre(
                id=row['id'], title_id=row['title_id'],
                genre_id=row['genre_id']
            )
            titlegenre.save()
