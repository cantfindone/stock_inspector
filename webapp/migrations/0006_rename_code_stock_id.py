# Generated by Django 4.1.1 on 2022-09-22 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0005_remove_stock_id_alter_stock_code"),
    ]

    operations = [
        migrations.RenameField(model_name="stock", old_name="code", new_name="id",),
    ]