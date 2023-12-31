# Generated by Django 4.2.5 on 2023-09-30 00:30

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fortune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=36, unique=True)),
                ('fortune', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Lantern',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nickname', models.CharField(max_length=10)),
                ('content', models.TextField(max_length=100)),
                ('password', models.CharField(max_length=4)),
                ('light_bool', models.BooleanField(blank=True, default=False)),
                ('is_liked', models.BooleanField(default=False)),
                ('is_reported', models.BooleanField(default=False)),
                ('lanternColor', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', multiselectfield.db.fields.MultiSelectField(choices=[('abuse', '욕설 및 비하'), ('fraud', '개인정보 유출 및 사칭, 사기'), ('explicit', '음란물 또는 불건전한 대화'), ('promotion', '영리목적이나 홍보성 게시글')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(max_length=36, null=True)),
                ('lantern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lantern.lantern')),
            ],
        ),
        migrations.CreateModel(
            name='LanternReaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike')], max_length=10)),
                ('user_id', models.CharField(max_length=36)),
                ('lantern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='lantern.lantern')),
            ],
        ),
    ]
