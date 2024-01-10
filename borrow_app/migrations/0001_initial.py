# Generated by Django 5.0.1 on 2024-01-10 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book_app', '0001_initial'),
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrowing_date', models.DateField(auto_now_add=True)),
                ('return_date', models.DateField(blank=True, null=True)),
                ('payment_status', models.CharField(choices=[('Payment Completed', 'PAID'), ('Refund Completed', 'REFUNDED')], default='PAID', max_length=20)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book_app.book')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.userprofile')),
            ],
        ),
    ]
