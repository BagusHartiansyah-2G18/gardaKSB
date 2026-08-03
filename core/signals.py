from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

# from .apps.keuangan.models import Pendapatan


# def recalculate_kas(kelompok_id):
#     saldo_kas = 0

#     data = (
#         Pendapatan.objects
#         .filter(usaha__kelompok_id=kelompok_id)
#         .order_by('dateCreate', 'id')
#     )

#     for item in data:
#         saldo_kas += item.laba

#         # update langsung ke database
#         # tidak memicu post_save lagi
#         # Pendapatan.objects.filter(
#         #     pk=item.pk
#         # ).update(
#         #     kas=saldo_kas
#         # )
#         Pendapatan.objects.update(
#             kas=saldo_kas
#         )


# @receiver(post_save, sender=Pendapatan)
# def pendapatan_saved(sender, instance, **kwargs):
#     recalculate_kas(instance.usaha.kelompok_id)


# @receiver(post_delete, sender=Pendapatan)
# def pendapatan_deleted(sender, instance, **kwargs):
#     recalculate_kas(instance.usaha.kelompok_id)