# Generated by Django 3.0.5 on 2020-05-04 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pizza',
            old_name='topping1',
            new_name='Main_Course',
        ),
        migrations.RenameField(
            model_name='pizza',
            old_name='topping2',
            new_name='Side_Dish',
        ),
    ]
