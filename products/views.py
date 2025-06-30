from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category, Subcategory, Product, ProductImage, Search
from cart.models import Cart, Order
from .errors import *
from .utils import open_session

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer

import os
from uuid import uuid4
import json
import jwt
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MARKS = [
    "Abarth", "Acura", "Aeon", "Aiways", "Aixam", "Alfa Romeo", "Alpina",
  "Alta", "AM General", "AMC", "Ariel", "Armstrong Siddeley", "Arrinera", 
  "Artega", "Ascari", "Aspark", "Aston Martin", "Audi", "Aurus", "Autobianchi",
  "BAIC", "Baojun", "BAC", "Bentley", "Bertone", "Bizzarrini", "Bollinger",
  "Borgward", "Brabus", "Bristol", "Brilliance", "Brooke", "Bufori", "Bugatti",
  "Buick", "BYD", "Callaway", "Canoo", "Caparo", "Caprice", "Carbodies", "Carlsson",
  "Casalini", "Caterham", "Changan", "Changfeng", "Chery", "Chevrolet", "Chrysler",
  "Cisitalia", "Citroën", "Cizeta", "Clenet", "Cupra", "Dacia", "Daewoo",
  "Daihatsu", "Dallara", "Datsun", "De Tomaso", "DeLorean", "Derways", "Detroit Electric",
  "Dodge", "Dongfeng", "Drako", "DS Automobiles", "Eagle", "Edsel", "Eicher Polaris",
  "Elemental", "Elfin", "EMC", "Emgrand", "Emil Frey", "Englon", "Equus", "Eterniti",
  "Excalibur", "FAW", "Faraday Future", "Ferrari", "Fiat", "Fisker", "Foday",
  "Force Motors", "Ford", "Foton", "GAC", "Galeon", "Geely", "Genesis", "Gibbs",
  "Gillet", "Ginetta", "GMC", "Gonow", "Great Wall", "Gumpert", "Hafei", "Haima",
  "Hanergy", "Haval", "Hennessey", "Hindustan", "Hino", "Holden", "Honda",
  "Hongqi", "Horch", "Hozon", "Hummer", "Hyundai", "Infiniti", "Iran Khodro",
  "Isdera", "Isuzu", "Italdesign", "Iveco", "JAC", "Jaguar", "Jeep", "Jensen",
  "Jetour", "Jetta", "Jinbei", "JMC", "Joylong", "Karma", "Karry", "Kia",
  "Koenigsegg", "Lada", "Lagonda", "Lamborghini", "Lancia", "Land Rover",
  "Landwind", "Leapmotor", "Lexus", "Lifan", "Ligier", "Lincoln", "Local Motors",
  "Lordstown", "Lotus", "Lucid", "Luxgen", "Mahindra", "Man", "Marcos",
  "Maserati", "Matra", "Maybach", "Mazda", "McLaren", "Mega", "Melkus",
  "Mercedes-AMG", "Mercedes-Benz", "Mercury", "Metrocab", "Microcar", "MINI",
  "Mitsuoka", "Mitsubishi", "Mobius Motors", "Morgan", "Morris", "Moskvich",
  "Nio", "Nissan", "Noble", "NSU", "Oldsmobile", "Omoda", "Opel", "ORA",
  "Pagani", "Panoz", "Peel", "Perodua", "Peugeot", "PGO", "Pininfarina",
  "Plymouth", "Polestar", "Pontiac", "Porsche", "Premier", "Proton", "Qoros",
  "Radical", "Rambler", "RAM", "Ravon", "Reliant", "Renault", "Rezvani", 
  "Rimac", "Rivian", "Roewe", "Rolls-Royce", "Rover", "Saab", "Sachsenring",
  "Saleen", "Samsung", "Saturn", "Scion", "SEAT", "Seres", "Shelby",
  "Shuanghuan", "Simca", "Singer", "Skoda", "Skywell", "Smart", "Soueast",
  "Spyker", "SsangYong", "Steyr", "Studebaker", "Subaru", "Suzuki", "Talbot",
  "Tarpan", "Tata", "Tatra", "Tesla", "Toyota", "Trabant", "Traum", "Trion",
  "Triumph", "TVR", "UAZ", "Ultima", "Vauxhall", "Vencer", "Venucia", "Vector",
  "VGV", "VinFast", "Volkswagen", "Volvo", "Vortex", "Voyah", "W Motors",
  "Wanderer", "Wartburg", "Wey", "Westfield", "Willys", "Wuling", "Yugo",
  "ZAZ", "Zenos", "Zenvo", "Zhongxing", "Zotye", "ZX Auto"
]

GENERATIONS = [
    "1950-1955",
    "1956-1960",
    "1961-1965",
    "1966-1970",
    "1971-1975",
    "1976-1980",
    "1981-1985",
    "1986-1990",
    "1991-1995",
    "1996-2000",
    "2001-2005",
    "2006-2010",
    "2011-2015",
    "2016-2020",
    "2021-2025"
]

def to_main(request):
    return HttpResponseRedirect('/products')

def products_page(request):
    open_session(request=request)
    context = {}
    page = request.GET.get('page') or 1
    search = request.GET.get('search')
    filter_name = request.GET.get('filter_name')
    filter_category = request.GET.get('filter_category')
    filter_subcategory = request.GET.get('filter_subcategory')
    filter_mark = request.GET.get('filter_mark')
    filter_model = request.GET.get('filter_model')
    filter_generation = request.GET.get('filter_generation')
    filter_quality = request.GET.get('filter_quality')
    filter_state = request.GET.get('filter_state')

    # для начала берем всю продукцию
    products = Product.objects.all()

    # собираем категории
    categoryes = Category.objects.all()

    # получаем данные о тележке
    cart = Cart.objects.get(id=request.session['cart'])
    

    if filter_name:
        products = products.filter(name=filter_name)
    if filter_category:
        category = Category.objects.get(id=filter_category)
        products = products.filter(category=category)
    if filter_subcategory:
        subcategory = Subcategory.objects.get(id=filter_subcategory)
        products = products.filter(subcategory=subcategory)
    if filter_mark:
        products = products.filter(mark=filter_mark)
    if filter_model:
        products = products.filter(model=filter_model)
    if filter_generation:
        products = products.filter(generation=filter_generation)
    if filter_quality:
        products = products.filter(quality=filter_quality)
    if filter_state:
        products = products.filter(state=filter_state)
    if search:
        products = products.filter(Q(name__icontains=search) | Q(mark__icontains=search) | Q(model__icontains=search))

    # paginator = Paginator(products, per_page=10)
    # products = paginator.get_page(page)
    context['products'] = products
    context['categoryes'] = categoryes
    context['cart'] = cart

    return render(request, 'products/main.html', context=context)


def current_product(request, product_id):
    product = Product.objects.get(id=product_id)
    products = Product.objects.all()
    cart = Cart.objects.get(id=request.session['cart'])
    context = {
        'cart': cart,
        'product': product,
        'products': products
    }
    
    return render(request, 'products/product.html', context=context)

def to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id=request.session['cart'])

    # Проверим, есть ли уже Order с таким продуктом в корзине
    existing_order = cart.products.filter(product=product).first()

    if existing_order:
        # Убираем этот Order из корзины
        cart.products.remove(existing_order)
        existing_order.delete()  # Удалим объект Order, если он больше нигде не нужен
    else:
        # Создаем и добавляем новый Order
        new_order = Order.objects.create(product=product)
        cart.products.add(new_order)
    return HttpResponseRedirect('/products')

def create_category(request):
    name = request.POST.get('name')
    if not Category.objects.get(name=name):
        category = Category.objects.create(name=name)
        return HttpResponseRedirect('/products')
    
    return HttpResponseRedirect(f'/products?error={ERROR_CATEGORY_EXIST}')


def create_subcategory(request, current_category):
    name = request.POST.get('name')

    category = Category.objects.get(id=current_category)
    if not Subcategory.objects.get(name=name, category=category):
        subcategory = Subcategory.objects.create(name=name, category=category)
        return HttpResponseRedirect('/products')
    
    return HttpResponseRedirect(f'/products?error={ERROR_SUBCATEGORY_EXIST}')


def my_cart(request):
    cart = Cart.objects.get(id=request.session['cart'])
    products = cart.products.all()
    products_count = 0
    products_price = 0

    for order in cart.products.all():
        products_count += order.count
        products_price += order.product.price * order.count

    context = {
        'cart': cart,
        'products': products,
        'products_count': products_count,
        'products_price': int(products_price)
    }

    return render(request, 'cart/main.html', context=context)


def product_add(request, product_id):
    cart = get_object_or_404(Cart, id=request.session['cart'])
    product = get_object_or_404(Product, id=product_id)

    # Пытаемся найти уже существующий Order для этого продукта в корзине
    order = cart.products.filter(product=product).first()

    if order:
        if product.count >= order.count + 1:
            order.count += 1
            order.save()
    else:
        order = Order.objects.create(product=product, count=1)
        cart.products.add(order)

    return HttpResponseRedirect('/products/myCart')


def product_remove(request, product_id):
    cart = get_object_or_404(Cart, id=request.session['cart'])
    product = get_object_or_404(Product, id=product_id)

    order = cart.products.filter(product=product).first()

    if order:
        if order.count > 1:
            order.count -= 1
            order.save()
        else:
            cart.products.remove(order)
            order.delete()

    return HttpResponseRedirect('/products/myCart')

def product_delete(request, product_id):
    cart = get_object_or_404(Cart, id=request.session['cart'])
    product = get_object_or_404(Product, id=product_id)

    order = cart.products.filter(product=product).first()

    if order:
        cart.products.remove(order)
        order.delete()

    return HttpResponseRedirect('/products/myCart')


def bye_cart(request):
    cart = get_object_or_404(Cart, id=request.session['cart'])
    products = cart.products.all()

    products_count = 0
    products_price = 0

    for order in cart.products.all():
        products_count += order.count
        products_price += order.product.price * order.count

    context = {
        'cart': cart,
        'products': products,
        'products_count': products_count,
        'products_price': products_price
    }

    data = request.GET
    if data:
        submit_bye(cart=cart, data=data)
        context['info'] = 'submited'

    
    return render(request, 'cart/bye.html', context=context)


def submit_bye(cart, data):
    for product in cart.products.all():
        product_ = Product.objects.get(id=product.product.id)
        product_.count -= product.count
        product_.save()
    
    cart.products.set([])


def search_queryset(queryset, search_query):
    from django.db.models import Q, CharField, TextField

    model = queryset.model

    if not search_query:
        return queryset.none()

    search_words = search_query.strip().split()
    search_words = [*search_words, *[x.capitalize() for x in search_words], *[x.lower() for x in search_words], *[x.upper() for x in search_words]]
    print(search_words)
    text_fields = [
        field.name for field in model._meta.get_fields()
        if isinstance(field, (CharField, TextField))
    ]

    print("Поиск по полям:", text_fields)

    if not text_fields:
        return queryset.none()

    query = Q()
    for word in search_words:
        word_q = Q()
        for field in text_fields:
            word_q |= Q(**{f"{field}__icontains": word})
        query |= word_q  # замените на |= для поиска хотя бы одного слова
    return queryset.filter(query).distinct()


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class GetProductsAPI(APIView):
    def get(self, request):
        ''' prouduct_id: uuid|str '''
        if product_id := request.GET.get('productId'):
            products = Product.objects.filter(id=product_id)
        else:
            products = Product.objects.all()

        search = request.GET.get('searchText')
        filter_name = request.GET.get('name')
        filter_category = request.GET.get('categoryId')
        filter_subcategory = request.GET.get('subcategoryId')
        filter_mark = request.GET.get('mark')
        filter_model = request.GET.get('model')
        filter_generation = request.GET.get('generation')
        filter_quality = request.GET.get('quality')
        filter_state = request.GET.get('state')

        if filter_name:
            products = products.filter(name=filter_name)
        if filter_category:
            category = Category.objects.get(id=filter_category)
            products = products.filter(category=category)
        if filter_subcategory:
            subcategory = Subcategory.objects.get(id=filter_subcategory)
            products = products.filter(subcategory=subcategory)
        if filter_mark:
            products = products.filter(mark=filter_mark)
        if filter_model:
            products = products.filter(model=filter_model)
        if filter_generation:
            products = products.filter(generation=filter_generation)
        if filter_quality:
            products = products.filter(quality=filter_quality)
        if filter_state:
            products = products.filter(state=filter_state)
        if search:
            search_object = Search.objects.create(text=search)
            # search = search.lower()
            products = search_queryset(products, search)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.POST
        if access_token := data.get('access_token'):
            if p := jwt.decode(access_token, 'test_admin_key'):
                if not p.get('is_admin'):
                    return Response({'error': 'Unauthorized exception'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Unauthorized exception'}, status=status.HTTP_401_UNAUTHORIZED)

        name = data.get('name') or '-'
        quality = data.get('quality') or 'Новое'
        mark = data.get('mark') or '-'
        model = data.get('model') or '-'
        count = data.get('count') or 0
        category = data.get('category') or None
        generation = data.get('generation') or '-'
        subcategory = data.get('subcategory') or None
        vincode = data.get('vincode') or '-'
        state = data.get('state') or '-'
        price = data.get('price') or 0
        unit = data.get('unit') or 'шт'
        part_number = data.get('partNumber') or '-'

        mark, model = mark.lower(), model.lower()

        if not category or not subcategory:
            return Response({'error': 'Не все поля заполнены'}, status=status.HTTP_409_CONFLICT)
        
        category = Category.objects.get(id=category)
        subcategory = Subcategory.objects.get(id=subcategory)
        images = request.FILES.getlist('images')

        saved_files = []

        for image in images:
            # Генерируем уникальное имя файла (например UUID)
            extension = os.path.splitext(image.name)[1]  # .jpg, .png
            filename = f"{uuid4()}{extension}"
            file_path = os.path.join('static/uploaded/', filename)

            # Сохраняем файл на диск
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            file_path = file_path.replace('static/','')
            # Сохраняем пути для дальнейшей работы
            # saved_files.append(os.path.join('uploads', filename))
            product_image = ProductImage.objects.create(file=file_path)
            saved_files.append(product_image)
        
        product = Product.objects.create(name=name,
                                        quality=quality,
                                        mark=mark,
                                        model=model,
                                        count=count,
                                        category=category,
                                        subcategory=subcategory,
                                        vincode=vincode,
                                        state=state,
                                        price=price,
                                        unit_of_m=unit,
                                        part_number=part_number,
                                        generation=generation)
        
        for image in saved_files:
            product.images.add(image)
        product.save()

        return Response({'result': 'success', 'productId': str(product.id)}, status=status.HTTP_201_CREATED)
    
    def patch(self, request):
        data = request.POST
        print(data)
        if access_token := data.get('access_token'):
            if p := jwt.decode(access_token, 'test_admin_key'):
                if not p.get('is_admin'):
                    return Response({'error': 'Unauthorized exception'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Unauthorized exception'}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = data.get('productId')
        name = data.get('name') or '-'
        quality = data.get('quality') or 'Новое'
        mark = data.get('mark') or '-'
        model = data.get('model') or '-'
        count = data.get('count') or 0
        category = data.get('category') or None
        generation = data.get('generation') or '-'
        subcategory = data.get('subcategory') or None
        vincode = data.get('vincode') or '-'
        state = data.get('state') or '-'
        price = data.get('price') or 0
        unit = data.get('unit') or 'шт'
        part_number = data.get('partNumber') or '-'
        image_ids = data.getlist('imageId')

        mark, model = mark.lower(), model.lower()

        if not category or not subcategory:
            return Response({'error': 'Не все поля заполнены'}, status=status.HTTP_409_CONFLICT)
        
        category = Category.objects.get(id=category)
        subcategory = Subcategory.objects.get(id=subcategory)
        product = Product.objects.get(id=product_id)

        product.name = name
        product.quality = quality
        product.mark = mark
        product.count = count
        product.category = category
        product.generation = generation
        product.subcategory = subcategory
        product.vincode = vincode
        product.state = state
        product.price = price
        product.unit_of_m = unit
        product.part_number = part_number

        print('img ids', image_ids)

        product_images = product.images.all()
        for image in product_images:
            print(str(image.id), image_ids)
            if not str(image.id) in image_ids:
                product.images.remove(image)  

        images = request.FILES.getlist('images')

        saved_files = []

        for image in images:
            # Генерируем уникальное имя файла (например UUID)
            extension = os.path.splitext(image.name)[1]  # .jpg, .png
            filename = f"{uuid4()}{extension}"
            file_path = os.path.join('static/uploaded/', filename)

            # Сохраняем файл на диск
            with open(file_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            file_path = file_path.replace('static/','')
            # Сохраняем пути для дальнейшей работы
            # saved_files.append(os.path.join('uploads', filename))
            product_image = ProductImage.objects.create(file=file_path)
            saved_files.append(product_image)

        for file in saved_files:
            product.images.add(file)

        product.save()

        return Response({'result': f'product {product_id} update success'})



    def delete(self, request):
        ''' productId: uuid|str '''
        if product_id := request.GET.get('productId'):
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response({'result': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'productId field is required'}, status=status.HTTP_409_CONFLICT)

class GetImageAPI(APIView):
    def get(self, request):
        ''' imageId: str '''
        data = request.GET
        image_id = data.get('imageId')

        try:
            image = ProductImage.objects.get(id=image_id)
        except:
            return Response({'error': 'file not found from db'}, status=status.HTTP_404_NOT_FOUND)
        try:
            if not 'static' in image.file:
                image.file = 'static/' + image.file
            file = open(image.file, 'rb')
            return FileResponse(file)
        except:
            return Response({'error': 'file not found'}, status=status.HTTP_404_NOT_FOUND)
        
class CategoryesAPI(APIView):
    def get(self, request):
        ''' categoryId: uuid|str '''
        if category_id := request.GET.get('categoryId'):
            categoryes = Category.objects.filter(id=category_id)
        else:
            categoryes = Category.objects.all()

        serializer = CategorySerializer(categoryes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class SubcategoryesAPI(APIView):
    def get(self, request):
        ''' 
            subcategoryId: uuid|str
            categoryId: uuid:str 
        '''
        if category_id := request.GET.get('categoryId'):
            category = Category.objects.get(id=category_id)
            subcategoryes = Subcategory.objects.filter(category=category)
        elif subcategory_id := request.GET.get('subcategoryId'):
            subcategoryes = Subcategory.objects.filter(id=subcategory_id)
        else:
            subcategoryes = Subcategory.objects.all()

        serializer = SubcategorySerializer(subcategoryes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request):
        ''' categoryId: uuid|str '''
        if access_token := json.loads(request.body).get('access_token'):
            if p := jwt.decode(access_token, 'test_admin_key'):
                if not p.get('is_admin'):
                    return Response({'error': 'Unauthorized exception'}, status=status.HTTP_401_UNAUTHORIZED)
                
        category_id = json.loads(request.body)
        category_id = category_id.get('categoryId')
        
        try:
            category = Category.objects.get(id=category_id)
        except:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        data = json.loads(request.body)
        if name := data.get('name'):
            subcategory = Subcategory.objects.create(name=name, category=category)
            return Response({'result': 'success', 'subcategoryId': str(subcategory.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'name field is required'}, status=status.HTTP_409_CONFLICT)

    def delete(self, request):
        ''' subcategoryId: str '''
        if subcategory_id := request.GET.get('subcategoryId'):
            subcategory = Subcategory.objects.get(id=subcategory_id)
            subcategory.delete()
        return Response({'result': 'success'}, status=status.HTTP_201_CREATED)
    

class ProductsActionsAPI(APIView):
    def post(self, request):
        ''' 
            productId: uuid|str
            action: str
        '''
        data = json.loads(request.body)

        product_id = data.get('productId')
        action = data.get('action') # remove | add

        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response({'error': 'product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if action == 'add':
            product.count += 1
        elif action == 'remove':
            product.count -= 1
        
        product.save()
        return Response({'result': 'success'}, status=status.HTTP_200_OK)


class CartAPI(APIView):
    def get(self, request):
        ''' cartId: uuid|str '''
        if cart_id := request.GET.get('cartId'):
            carts = Cart.objects.filter(id=cart_id)
        else:
            carts = Cart.objects.all()

        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''
            products: [{productId: uuid: str, count: int}]
        '''
        # form_data = request.POST.get('formData')
        '''
        {
            name: "",
            phone: "",
            address: "",
            additional_phone: "",
            promocode: "",
        }
        '''
        # print(request.body)
        products = json.loads(request.body).get('products')
        print(products)
        cart = Cart.objects.create()
        for p in products:
            product = Product.objects.get(id=p['product_id'])
            count = p['count']

            product.count -= count
            product.save()

            order = Order.objects.create(product=product, count=count)
            cart.products.add(order)
            cart.save()
        
        return Response({'result': 'success', 'cartId': str(cart.id)})
    

class FiltersAPI(APIView):
    def get(self, request):
        models = []
        with open('car_models_extended.json') as f:
            models = json.loads(f.read())

        products = Product.objects.all()
        models_ = {}



        for product in products:
            if product.mark:
                if not product.mark.lower().strip() in models_:
                    models_[product.mark.lower().strip()] = []
            if product.model and models_[product.mark.lower().strip()] != None:
                current_model = {
                    'id': len( models_[product.mark.lower().strip()]) + 1,
                    'value': product.model.lower().strip()
                }
                if not current_model in models_[product.mark.lower().strip()]:
                    models_[product.mark.lower().strip()].append(
                        current_model
                    )
        
        # for model in models:
        #     models_[model['mark']] = model['options']
        print(models_)

        generations = list(set([
            product.generation.lower().strip() for product in products
        ]))

        return Response(
            [
                {
                    'filter': 'Марка авто',
                    'options': [
                        {
                            'id': index,
                            'value': value
                        } for index, value in enumerate(list(models_.keys()))
                    ]
                },
                {
                    'filter': 'Модель',
                    'options': [
                        models_
                    ]
                },
                {
                    'filter': 'Поколение',
                    'options': [
                        {
                            'id': index,
                            'value': value
                        } for index, value in enumerate(generations)
                    ]
                },
                {
                    'filter': 'Качество',
                    'options': [
                        {
                            'id': 1,
                            'value': 'Оригинал'
                        },
                        {
                            'id': 2,
                            'value': 'Дубликат'
                        }, 
                    ]
                },
                {
                    'filter': 'Состояние',
                    'options': [
                        {
                            'id': 1,
                            'value': 'Новая'
                        },
                        {
                            'id': 2,
                            'value': 'Б/У'
                        }, 
                    ]
                }
            ],
        status=status.HTTP_200_OK)
    

class AdminAuthAPI(APIView):
    def get(self, request):
        admin_login = os.getenv('ADMIN_LOGIN')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if admin_login == request.GET.get('login') and admin_password == request.GET.get('password'):
            token = jwt.encode({'is_admin': True}, key='test_admin_key').decode()
            return Response({'token': token}, status=status.HTTP_200_OK)
        
        return Response({'error': 'Unauthorized exception'}, status=status.HTTP_401_UNAUTHORIZED)
    

class StatisticAPI(APIView):
    def get(self, request):
        carts = Cart.objects.all()
        parts = {}
        dates = [cart.date.strftime('%d %m %Y') for cart in carts]
        dates = list(set(dates))

        for date in dates:
            for cart in carts:
                if date == cart.date.strftime('%d %m %Y'):
                    if not parts.get(date):
                        parts[date] = 0
                    parts[date] += 1
        
        return Response({'result': parts}, status=status.HTTP_200_OK)
        

class SearchAPI(APIView):
    def post(self, request):
        ''' search: str '''
        data = json.loads(request.body)

        search_text = data.get('search')
        search = Search.objects.create(text=search_text)

        return Response({'result': 'success'}, status=status.HTTP_201_CREATED)
    
    def get(self, request):
        searches = Search.get_top_search_queries(limit=100)

        return Response({'result': searches}, status=status.HTTP_200_OK)

# Product.upload_from_parts(name='parts.xlsx')