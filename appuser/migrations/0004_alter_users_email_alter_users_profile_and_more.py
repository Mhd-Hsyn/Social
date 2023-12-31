# Generated by Django 4.2.4 on 2023-08-21 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0003_users_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=models.ImageField(blank=True, default='user_default/default_img.png', upload_to='my_picture'),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.CreateModel(
            name='UserPost',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appuser.basemodel')),
                ('image', models.ImageField(default=None, upload_to='post_picture')),
                ('caption', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.users')),
            ],
            bases=('appuser.basemodel',),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appuser.basemodel')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.userpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.users')),
            ],
            bases=('appuser.basemodel',),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='appuser.basemodel')),
                ('text', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.userpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.users')),
            ],
            bases=('appuser.basemodel',),
        ),
    ]
