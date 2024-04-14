# Generated by Django 5.0.3 on 2024-04-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_rename_diray_diary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('no', models.IntegerField()),
                ('sex', models.BooleanField(default=False)),
                ('byear', models.IntegerField()),
                ('party', models.CharField(max_length=20)),
                ('votes', models.IntegerField()),
            ],
        ),
    ]
