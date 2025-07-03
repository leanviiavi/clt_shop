from django.db import models
from uuid import uuid4
from datetime import datetime


class Category(models.Model):
    ''' Категория продукции '''
    id = models.UUIDField(default=uuid4, primary_key=True)

    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    ''' Подкатегория продукции '''
    id = models.UUIDField(default=uuid4, primary_key=True)

    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    ''' Изображение продукта '''
    id = models.UUIDField(default=uuid4, primary_key=True)

    file = models.CharField(max_length=256)


class Product(models.Model):
    ''' Продукт '''
    id = models.UUIDField(default=uuid4, primary_key=True)

    name = models.CharField(max_length=128, default='-', null=True, blank=True)
    mark = models.CharField(max_length=32, default='-', null=True, blank=True)
    model = models.CharField(max_length=128, default='-', null=True, blank=True)
    generation = models.CharField(max_length=16, default='-', null=True, blank=True)
    vincode = models.CharField(max_length=32, default='-', null=True, blank=True)
    quality = models.CharField(max_length=16, default='-', null=True, blank=True)
    state = models.CharField(max_length=32, default='Новое', null=True, blank=True)
    unit_of_m = models.CharField(max_length=32, default='шт', null=True, blank=True)
    count = models.IntegerField(default=0)
    part_number = models.CharField(max_length=32, default='-', null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    price = models.FloatField(default=0.0)
    images = models.ManyToManyField(ProductImage, 'images')
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    @staticmethod
    def upload_from_parts(name: str):
        import pandas as pd
        Product.objects.all().delete()
        df = pd.read_excel("parts.xlsx")
        desired_columns = df.columns.tolist()
        parts_list = df.to_dict(orient="records")

        # desired_columns = [
        #     'Партномер запчасти', 'Марка авто', 'Модель авто', 'Название запчасти',
        #     'Категория', 'Подкатегория', 'Качество', 'Состояние',
        #     'Поколение', 'Единица изм', 'Винкод', 'Цена', 'Количество'
        # ]

        df = pd.read_excel(name, usecols=desired_columns)
        parts_list = df.to_dict(orient="records") 
        for part in parts_list:
            if not Category.objects.filter(name=part['Категория']):
                category = Category.objects.create(name=part['Категория'])
            else:
                category = Category.objects.get(name=part['Категория'])

            if not Subcategory.objects.filter(name=part['Подкатегория'], category=category):
                subcategory = Subcategory.objects.create(name=part['Подкатегория'], category=category)
            else:
                subcategory = Subcategory.objects.get(name=part['Подкатегория'], category=category)

            
            product = Product.objects.create(
                name=part['Название запчасти'],
                mark=part['Марка авто'],
                model=part['Модель авто'],
                generation=part['Поколение'],
                vincode=part['Винкод'],
                quality=part['Качество'],
                state=part['Состояние'],
                unit_of_m=part['Еденица измерения'],
                count=1,
                part_number=part['Партномер запчасти'],
                rating=0,
                category=category,
                subcategory=subcategory,
            )
            product.images.set(ProductImage.objects.filter(id='0267be89-a0c0-45e1-be5e-0944a4baf36c'))

            print(f'uploaded {product.id}')


class Search(models.Model):
    ''' Поисковый запрос '''
    id = models.UUIDField(default=uuid4, primary_key=True)

    date = models.DateTimeField(default=datetime.now, blank=True)
    text = models.CharField(max_length=128, default='', null=True, blank=True)

    def get_top_search_queries(limit=10):
        """
        Возвращает список самых популярных поисковых запросов.
        
        :param limit: количество самых популярных запросов, по умолчанию 10
        :return: список словарей с ключами 'text' и 'count'
        """
        top_queries = (
            Search.objects
            .filter(text__isnull=False)  # исключаем пустые или None значения
            .exclude(text='')           # исключаем пустые строки
            .values('text')
            .annotate(count=models.Count('text'))
            .order_by('-count')[:limit]
        )
        return list(top_queries)