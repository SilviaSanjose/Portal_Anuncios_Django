# Generated by Django 3.0.6 on 2020-05-18 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0005_auto_20200518_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.FileField(null=True, upload_to='anuncios/static/perfiles'),
        ),
    ]
