# Generated by Django 3.1.4 on 2021-02-15 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=50, verbose_name='İçerik'),
        ),
    ]
