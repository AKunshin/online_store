import stripe
from loguru import logger
from django.conf import settings
from django.db import models

# logger.add(level="DEBUG")


stripe.api_key = settings.STRIPE_SECRET_KEY


class Discount(models.Model):
    """Модель скидки"""
    DURATION = (
        ("once", "ONCE"),
        ("forever", "FOREVER"),
        ("repeating", "REPEATING"),
    )
    name = models.CharField(max_length=20,
                            verbose_name="Название купона")
    percent_off = models.IntegerField(
        verbose_name="Процент скидки")
    duration = models.CharField(
        max_length=20,
        choices=DURATION,
        default="once",
        verbose_name="Срок действия")

    @logger.catch
    def save(self, *args, **kwargs):
        """Функция для создания промокода в Stripe"""
        promocode_list = stripe.PromotionCode.list()
        coupons = Discount.objects.all()
        if coupons.count() >= 1:

            try:
                stripe_active_promocodes = []
                for promocode in promocode_list:
                        # logger.debug(f"promocode.active: {promocode.active}")
                        # logger.info(f"promocode: {type(promocode.code)}")
                        if promocode.active:
                            stripe_active_promocodes += [promocode.code]
                            logger.debug(f"Active promocodes: {stripe_active_promocodes}")
                            # new_coupon=promocode.coupon.id

                for coupon in coupons:
                    logger.debug(f"Coupon in DB {coupon.name}")
                    logger.debug(f"Coupon percent_off {coupon.percent_off}")
                    if coupon.name in stripe_active_promocodes:
                        logger.error(
                            f"Промокод с именем {coupon.name} уже есть")
                        continue             
                                
                    stripe_coupon = stripe.Coupon.create(
                        percent_off=coupon.percent_off,
                        duration=coupon.duration,
                    )
                    new_coupon=stripe_coupon.id
                    logger.debug(f"Создан купон {stripe_coupon.id}")

                    promocode_stripe = stripe.PromotionCode.create(
                        coupon=new_coupon,
                        code=coupon.name,
                    )
                    logger.debug(f"Создан промокод {promocode_stripe.code}")

                # raise Exception("Указанные промокоды уже существуют")

            except Exception as e:
                print(f"Exception by create discount {e}")
        else:
            print("В БД не найдено ни одного купона")
        return super(Discount, self).save(*args, **kwargs)
