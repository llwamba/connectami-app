# Generated by Django 4.0 on 2023-09-07 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('connectamiapp_comment', '0001_initial'),
        ('connectamiapp_user', '0001_initial'),
        ('connectamiapp_post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connectamiapp_user.user'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='connectamiapp_post.post'),
        ),
    ]
