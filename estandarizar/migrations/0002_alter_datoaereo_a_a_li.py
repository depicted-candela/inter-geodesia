# Generated by Django 4.2.8 on 2023-12-09 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estandarizar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datoaereo',
            name='a_a_li',
            field=models.DecimalField(decimal_places=2, help_text='Anomalía de aire libre', max_digits=6, null=True),
        ),
    ]
