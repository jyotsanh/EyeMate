# Generated by Django 5.0.6 on 2024-06-18 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_productimage_image_url_alter_review_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image_url',
            field=models.ImageField(upload_to='products/'),
        ),
    ]
