# Generated by Django 4.2 on 2023-04-28 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('published_date', models.DateTimeField()),
                ('media', models.ImageField(upload_to='news-media/%Y/%m/%d/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.categories')),
            ],
        ),
    ]