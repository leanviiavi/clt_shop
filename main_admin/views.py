from django.shortcuts import render
from django.http import HttpResponseRedirect

from products.models import Category, Subcategory, Product, ProductImage
from products.errors import *

import os
from uuid import uuid4
from dotenv import load_dotenv
load_dotenv()


def main(request):
    if not request.session.get('is_admin'):
        return HttpResponseRedirect('/admin/auth')
    
    categoryes = Category.objects.all()
    products = Product.objects.all()

    filter_name = request.GET.get('filter_name')
    filter_category = request.GET.get('filter_category')
    filter_subcategory = request.GET.get('filter_subcategory')
    filter_mark = request.GET.get('filter_mark')
    filter_model = request.GET.get('filter_model')
    filter_generation = request.GET.get('filter_generation')
    filter_quality = request.GET.get('filter_quality')
    filter_state = request.GET.get('filter_state')

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

    context = {
        'products': products,
        'categoryes': categoryes,
    }

    return render(request, 'admin/main.html', context=context)


def add(request, product_id):
    product = Product.objects.get(id=product_id)
    product.count += 1
    product.save()

    return HttpResponseRedirect('/admin')

def remove(request, product_id):
    product = Product.objects.get(id=product_id)
    product.count -= 1
    if not product.count < 0:
        product.save()

    return HttpResponseRedirect('/admin')

def delete(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()

    return HttpResponseRedirect('/admin')


def add_category(request):
    name = request.POST.get('name')
    if not Category.objects.filter(name=name):
        category = Category.objects.create(name=name)
        return HttpResponseRedirect('/admin')
    
    return HttpResponseRedirect(f'/admin?error={ERROR_CATEGORY_EXIST}')

def add_subcategory(request, current_category):
    name = request.POST.get('name')

    category = Category.objects.get(id=current_category)
    if not Subcategory.objects.filter(name=name, category=category):
        subcategory = Subcategory.objects.create(name=name, category=category)
        return HttpResponseRedirect('/admin')
    
    return HttpResponseRedirect(f'/admin?error={ERROR_SUBCATEGORY_EXIST}')


def new_product(request):
    categoryes = Category.objects.all()
    subcategoryes = Subcategory.objects.all()
    error = request.GET.get('error') or ''
    marks = [
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
    generations = [
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
    context={
        'categoryes': categoryes,
        'subcategoryes': subcategoryes,
        'generations': generations,
        'marks': marks,
        'error': error
    }
    return render(request, 'admin/new_product.html', context=context)

def add_new_product(request):
    data = request.POST

    name = data.get('name') or '-'
    quality = data.get('quality') or 'Новое'
    mark = data.get('mark') or '-'
    model = data.get('model') or '-'
    count = data.get('count') or 0
    category = data.get('category') or None
    subcategory = data.get('subcategory') or None
    vincode = data.get('vincode') or '-'
    state = data.get('state') or '-'
    price = data.get('price') or 0
    unit = data.get('unit') or 'шт'

    if not category or not subcategory:
        return HttpResponseRedirect('/admin/newProduct?error=Не все поля заполнены')

    category = Category.objects.get(id=category)
    subcategory = Subcategory.objects.get(id=subcategory)
    images = request.FILES.getlist('images')

    print(images)
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
                                     unit_of_m=unit)
    
    for image in saved_files:
        product.images.add(image)
    product.save()
    


    return HttpResponseRedirect('/admin')


def auth_page(request):
    error = request.GET.get('error') or ''
    context = {
        'error': error
    }
    return render(request, 'admin/auth.html', context=context)

def auth(request):
    data = request.POST
    login = data.get('login')
    password = data.get('password')


    admin_login = os.environ.get('ADMIN_LOGIN')
    admin_password = os.environ.get('ADMIN_PASSWORD')

    if not login or not password:
        return HttpResponseRedirect('/admin/auth?error=Неверный логин или пароль')
    
    if not admin_login == login or not admin_password == password:
        return HttpResponseRedirect('/admin/auth?error=Неверный логин или пароль')
    
    request.session['is_admin'] = True
    return HttpResponseRedirect('/admin')