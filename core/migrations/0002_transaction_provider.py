# Generated by Django 3.1.5 on 2021-02-01 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='provider',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='core.provider'),
            preserve_default=False,
        ),
    ]
