# Generated by Django 2.0.6 on 2018-06-12 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0002_auto_20180612_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
    ]
