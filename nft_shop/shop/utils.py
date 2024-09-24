import redis
from django.conf import settings
from django.db.models import QuerySet


r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def set_views_for_products(products: QuerySet) -> QuerySet:
    for p in products:
        result = r.get(f"nft:{p.id}:views")
        p.views = result.decode() if result is not None else 0

    return products
