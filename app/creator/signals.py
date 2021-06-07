"""
This is default Django Signals module.
You can define different Signals to add extra functionality
to your code before and/or after storing the data into database.

You can use different signal calls for that like pre_save, post_save etc.
"""

import boto3
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from pathlib import Path

from creator.models import CreatorClass, Material, Stream


@receiver(post_save, sender=CreatorClass)
def creator_class_post_save_receiver(sender, instance, raw, created, update_fields, **kwargs):
    """Fires a Signal after storing the Creator Class data into database"""

    if not instance.class_file:
        return False
    print("<<<-----|| SIGNAL FIRED = Creator Class (Post) ||----->>>")

    class_file = str(settings.ENDPOINT_URL) + str(instance.class_file)

    client = boto3.client(
        'elastictranscoder',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.REGION_NAME
    )

    in_key = class_file.split('.com/')[1]
    file_name = class_file.split('/classes/')[1]
    name = file_name.split(Path(file_name).suffix)[0]
    out_path = in_key.replace('/classes/', '/classes/transcoded/')
    out_key = out_path.split(file_name)[0]

    client.create_job(
        PipelineId=str(settings.AWS_PIPELINE_ID),
        Input={
            'Key': in_key,
        },
        Outputs=[
            {
                'Key': name + '.mp4',
                'PresetId': str(settings.AWS_PRESET_ID),
            },
        ],
        OutputKeyPrefix=out_key,
    )

    print("Job created successfully")

    new_file_name = class_file.split('/classes/')[1]
    new_name = new_file_name.split(Path(new_file_name).suffix)[0]

    new_path = class_file.replace('/classes/', '/classes/transcoded/')
    key1 = new_path.split('classes/transcoded/')[0]
    key2 = 'classes/transcoded/' + new_name + '.mp4'
    transcoded_class_file = key1 + key2
    CreatorClass.objects.filter(pk=instance.id).update(transcoded_class_file=transcoded_class_file)
    return


@receiver(post_save, sender=Material)
def creator_material_post_save_receiver(sender, instance, raw, created, update_fields, **kwargs):
    """Fires a Signal after storing the Creator Material data into database"""

    if not instance.material_file:
        return False
    print("<<<-----|| SIGNAL FIRED = Creator Material (Post) ||----->>>")

    material_file = str(settings.ENDPOINT_URL) + str(instance.material_file)

    client = boto3.client(
        'elastictranscoder',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.REGION_NAME
    )

    in_key = material_file.split('.com/')[1]
    file_name = material_file.split('/materials/')[1]
    name = file_name.split(Path(file_name).suffix)[0]
    out_path = in_key.replace('/materials/', '/materials/transcoded/')
    out_key = out_path.split(file_name)[0]

    client.create_job(
        PipelineId=str(settings.AWS_PIPELINE_ID),
        Input={
            'Key': in_key,
        },
        Outputs=[
            {
                'Key': name + '.mp4',
                'PresetId': str(settings.AWS_PRESET_ID),
            },
        ],
        OutputKeyPrefix=out_key,
    )

    print("Job created successfully")

    new_file_name = material_file.split('/materials/')[1]
    new_name = new_file_name.split(Path(new_file_name).suffix)[0]

    new_path = material_file.replace('/materials/', '/materials/transcoded/')
    key1 = new_path.split('materials/transcoded/')[0]
    key2 = 'materials/transcoded/' + new_name + '.mp4'
    transcoded_material_file = key1 + key2
    Material.objects.filter(pk=instance.id).update(transcoded_material_file=transcoded_material_file)
    return


@receiver(post_save, sender=Stream)
def creator_stream_post_save_receiver(sender, instance, raw, created, update_fields, **kwargs):
    """Fires a Signal after storing the Creator Stream data into database"""

    if not instance.sneak_peak_file:
        return False
    print("<<<-----|| SIGNAL FIRED = Creator Stream (Post) ||----->>>")
    sneak_peak_file = str(settings.ENDPOINT_URL) + str(instance.sneak_peak_file)
    print(sneak_peak_file)

    client = boto3.client(
        'elastictranscoder',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.REGION_NAME
    )

    in_key = sneak_peak_file.split('.com/')[1]
    file_name = sneak_peak_file.split('/streams/')[1]
    name = file_name.split(Path(file_name).suffix)[0]
    out_path = in_key.replace('/streams/', '/streams/transcoded/')
    out_key = out_path.split(file_name)[0]

    client.create_job(
        PipelineId=str(settings.AWS_PIPELINE_ID),
        Input={
            'Key': in_key,
        },
        Outputs=[
            {
                'Key': name + '.mp4',
                'PresetId': str(settings.AWS_PRESET_ID),
            },
        ],
        OutputKeyPrefix=out_key,
    )

    print("Job created successfully")

    new_file_name = sneak_peak_file.split('/streams/')[1]
    new_name = new_file_name.split(Path(new_file_name).suffix)[0]

    new_path = sneak_peak_file.replace('/streams/', '/streams/transcoded/')
    key1 = new_path.split('streams/transcoded/')[0]
    key2 = 'streams/transcoded/' + new_name + '.mp4'
    transcoded_sneak_peak_file = key1 + key2
    Stream.objects.filter(pk=instance.id).update(transcoded_sneak_peak_file=transcoded_sneak_peak_file)
    return
