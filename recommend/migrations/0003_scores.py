# Generated by Django 2.2.2 on 2019-07-15 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0002_customuser_newsongs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='sheetmusic')),
                ('song', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='recommend.Song')),
            ],
        ),
    ]
