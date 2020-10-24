# Generated by Django 3.1.2 on 2020-10-23 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Add',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hospital', models.CharField(max_length=100)),
                ('Beds_Cap', models.IntegerField()),
                ('Beds_occ', models.IntegerField()),
                ('Max_Vent', models.IntegerField()),
                ('Active_vent', models.IntegerField()),
                ('Active_Covid', models.IntegerField()),
                ('Max_ICU', models.IntegerField()),
                ('Active_ICU', models.IntegerField()),
            ],
        ),
    ]