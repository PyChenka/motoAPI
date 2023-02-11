# Generated by Django 4.1.6 on 2023-02-10 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='current_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bike', to='moto.owner'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='previous_owners',
            field=models.ManyToManyField(related_name='bikes', through='moto.Ownership', to='moto.owner'),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='date_purchase',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='date_sale',
            field=models.DateField(null=True),
        ),
    ]