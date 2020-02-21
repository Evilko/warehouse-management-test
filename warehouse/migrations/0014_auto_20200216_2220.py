# Generated by Django 3.0.3 on 2020-02-16 12:20

from django.db import migrations, models
import django.db.models.deletion


import datetime
import pytz


def fill(apps, schema_editor):
    Category = apps.get_model('warehouse', 'Category')
    Stock = apps.get_model('warehouse', 'Stock')
    Supplier = apps.get_model('warehouse', 'Supplier')
    Customer = apps.get_model('warehouse', 'Customer')
    Cargo = apps.get_model('warehouse', 'Cargo')
    Shipment = apps.get_model('warehouse', 'Shipment')
    CargoStock = apps.get_model('warehouse', 'CargoStock')
    ShipmentStock = apps.get_model('warehouse', 'ShipmentStock')
    SupplierCategory = apps.get_model('warehouse', 'SupplierCategory')

    now = datetime.datetime.now(tz=pytz.utc)
    last_week = now - datetime.timedelta(days=7)
    last_month = now - datetime.timedelta(days=31)

    categories = (Category(pk=1, name='Электроника', parent_id=0),
                  Category(pk=2, name='Бытовая техника', parent_id=0),
                  Category(pk=3, name='Телевизоры', parent_id=1),
                  Category(pk=4, name='Телефоны', parent_id=1),
                  Category(pk=5, name='Смартфоны', parent_id=4),
                  Category(pk=6, name='Холодильники', parent_id=2),
                  Category(pk=7, name='Стиральные машины', parent_id=2),
                  Category(pk=8, name='Посудомоечные машины', parent_id=2), )

    Category.objects.bulk_create(categories)

    stocks = (Stock(pk=100, category=categories[2],
                    name='Телевизор LG', price=10000,
                    number=10),
              Stock(pk=101, category=categories[2],
                    name='Телевизор Samsung', price=11000,
                    number=9),
              Stock(pk=102, category=categories[2],
                    name='Телевизор Sony', price=12000,
                    number=20),
              Stock(pk=103, category=categories[6],
                    name='Стиральная машина LG', price=10500,
                    number=5),
              Stock(pk=104, category=categories[4],
                    name='Смартфон Samsung Galaxy Note 8', price=13000,
                    number=18),
              Stock(pk=105, category=categories[5],
                    name='Холодильник LG', price=10000,
                    number=12),
              Stock(pk=106, category=categories[5],
                    name='Холодильник Samsung', price=15000,
                    number=0),
              )

    Stock.objects.bulk_create(stocks)

    suppliers = (Supplier(pk=1, organization='LG',
                          address='680000, Хабаровск, ул. Большая, 1-1',
                          phone_number='111111',
                          email='lg@domain.com',
                          legal_details='ИНН: 9909111111',
                          contact_info='Контактное лицо: Сергей Иванович Сидоров'),
                 Supplier(pk=2, organization='Samsung',
                          address='680000, Хабаровск, ул. Большая, 1-2',
                          phone_number='111112',
                          email='samsung@domain.com',
                          legal_details='ИНН: 9909111112',
                          contact_info='Контактное лицо: Сергей Иванович Семенов'),
                 Supplier(pk=3, organization='Sony',
                          address='680000, Хабаровск, ул. Большая, 1-3',
                          phone_number='111113',
                          email='sony@domain.com',
                          legal_details='ИНН: 9909111113',
                          contact_info='Контактное лицо: Сергей Иванович Петров'),
                 )
    Supplier.objects.bulk_create(suppliers)

    for i in range(7):
        SupplierCategory.objects.create(supplier=suppliers[0], category=categories[i])
        SupplierCategory.objects.create(supplier=suppliers[1], category=categories[i])
    for i in range(6):
        SupplierCategory.objects.create(supplier=suppliers[2], category=categories[i])

    customers = (Customer(pk=1, full_name='Иван Иванович Иванов',
                          phone_number='222222',
                          email='den_se_in@mail.ru',
                          contact_info='Контактное лицо: Иван Иванович Иванов'),
                 Customer(pk=2, full_name='Петр Петрович Петров',
                          phone_number='222223',
                          email='den_se_in@mail.ru',
                          contact_info='Контактное лицо: Петр Петрович Петров'),
                 Customer(pk=3, full_name='Светлана Семеновна Семенова',
                          phone_number='222224',
                          email='den_se_in@mail.ru',
                          contact_info='Контактное лицо: Светлана Семеновна Семенова'),
                 Customer(pk=4, full_name='Анна Николаевна Николаева',
                          phone_number='222225',
                          email='den_se_in@mail.ru',
                          contact_info='Контактное лицо: Анна Николаевна Николаева'),

                 )
    Customer.objects.bulk_create(customers)

    cargo = (Cargo(pk=1, supplier=suppliers[0],
                   date=last_week),
             Cargo(pk=2, supplier=suppliers[0],
                   date=last_month),
             Cargo(pk=3, supplier=suppliers[1],
                   date=last_week),
             Cargo(pk=4, supplier=suppliers[1],
                   date=last_week),
             Cargo(pk=5, supplier=suppliers[0],
                   date=last_week),
             )

    Cargo.objects.bulk_create(cargo)

    CargoStock.objects.create(cargo=cargo[0], stock=stocks[0], number=10)
    CargoStock.objects.create(cargo=cargo[1], stock=stocks[3], number=5)
    CargoStock.objects.create(cargo=cargo[1], stock=stocks[5], number=15)
    CargoStock.objects.create(cargo=cargo[2], stock=stocks[0], number=10)
    CargoStock.objects.create(cargo=cargo[2], stock=stocks[4], number=20)
    CargoStock.objects.create(cargo=cargo[3], stock=stocks[6], number=10)
    CargoStock.objects.create(cargo=cargo[4], stock=stocks[6], number=10)

    shipments = (Shipment(pk=1, customer=customers[0],
                          date=now),
                 Shipment(pk=2, customer=customers[0],
                          date=now),
                 Shipment(pk=3, customer=customers[0],
                          date=now),
                 Shipment(pk=4, customer=customers[1],
                          date=now),
                 Shipment(pk=5, customer=customers[2],
                          date=now),
                 Shipment(pk=6, customer=customers[0],
                          date=now),
                 Shipment(pk=7, customer=customers[1],
                          date=now),
                 Shipment(pk=8, customer=customers[2],
                          date=now),
                 )

    Shipment.objects.bulk_create(shipments)

    ShipmentStock.objects.create(shipment=shipments[0], stock=stocks[6], number=10)
    ShipmentStock.objects.create(shipment=shipments[1], stock=stocks[4], number=1)
    ShipmentStock.objects.create(shipment=shipments[2], stock=stocks[5], number=1)
    ShipmentStock.objects.create(shipment=shipments[3], stock=stocks[5], number=2)
    ShipmentStock.objects.create(shipment=shipments[4], stock=stocks[0], number=1)
    ShipmentStock.objects.create(shipment=shipments[0], stock=stocks[4], number=1)
    ShipmentStock.objects.create(shipment=shipments[6], stock=stocks[5], number=5)
    ShipmentStock.objects.create(shipment=shipments[4], stock=stocks[5], number=4)
    ShipmentStock.objects.create(shipment=shipments[5], stock=stocks[4], number=3)
    ShipmentStock.objects.create(shipment=shipments[7], stock=stocks[2], number=7)


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0013_auto_20200212_1005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cargostock',
            options={'verbose_name': 'Поставка', 'verbose_name_plural': 'Поставки'},
        ),
        migrations.AlterModelOptions(
            name='shipmentstock',
            options={'verbose_name': 'Покупка', 'verbose_name_plural': 'Покупки'},
        ),
        migrations.AlterModelOptions(
            name='suppliercategory',
            options={'verbose_name': 'Категория поставщиков', 'verbose_name_plural': 'Категории поставщиков'},
        ),
        migrations.AlterField(
            model_name='cargostock',
            name='cargo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Cargo'),
        ),
        migrations.AlterField(
            model_name='cargostock',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Stock'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=80, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_id',
            field=models.IntegerField(default=0, verbose_name='Базовая категория'),
        ),
        migrations.AlterField(
            model_name='shipmentstock',
            name='shipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Shipment'),
        ),
        migrations.AlterField(
            model_name='shipmentstock',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Stock'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='categories',
            field=models.ManyToManyField(through='warehouse.SupplierCategory', to='warehouse.Category'),
        ),
        migrations.AlterField(
            model_name='suppliercategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Category'),
        ),
        migrations.AlterField(
            model_name='suppliercategory',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Supplier'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'parent_id')},
        ),
        migrations.RunPython(fill)
    ]
