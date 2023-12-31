# Generated by Django 4.2.3 on 2023-07-13 07:09

from django.db import migrations, models
import django.db.models.deletion
import playlist.models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0003_album_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='image',
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=playlist.models.image_upload_path)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='playlist.album')),
            ],
        ),
    ]
