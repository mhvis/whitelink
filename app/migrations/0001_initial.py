# Generated by Django 3.1.4 on 2020-12-19 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WhitelistEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(db_index=True)),
                ('friendly_name', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
    ]
