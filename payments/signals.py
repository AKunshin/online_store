import stripe

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from loguru import logger

from payments.models import Discount


stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(post_save, sender=Discount)
def create_stripe_coupon(sender, instance, **kwargs):
    """Функция для создания купона в Stripe"""
    discount = instance
    try:
        stripe_coupon = stripe.Coupon.create(
            id=discount.name,
            percent_off=discount.percent_off,
            duration=discount.duration,
        )
        new_coupon = stripe_coupon.id

        promocode_stripe = stripe.PromotionCode.create(
            coupon=new_coupon,
            code=discount.name,
        )

    except Exception as e:
        logger.error(f"Exception by create coupon: {e}")


@receiver(post_delete, sender=Discount)
def delete_stripe_coupon(sender, instance, *args, **kwargs):
    """Функция для удаления купона в Stripe"""
    try:
        stripe.Coupon.delete(instance.name)
    except Exception as e:
        logger.error(f"Exception by delete coupon: {e}")
