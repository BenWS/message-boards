# Generated by Django 3.0 on 2020-09-26 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20200922_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='topics', to='boards.Topic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='board',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='topics', to='boards.Board'),
            preserve_default=False,
        ),
    ]
