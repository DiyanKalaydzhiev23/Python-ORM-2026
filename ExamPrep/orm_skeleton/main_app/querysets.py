from django.db.models import QuerySet, Count


class ProfileQueryset(QuerySet):
    def get_regular_customers(self) -> QuerySet:
        """
        SELECT
            *,
            COUNT(*) AS count_orders,
        FROM
            profiles
        JOIN
            orders
        ON
            ...
        GROUP BY
            profile.id
        HAVING
            count_orders > 2
        ORDER BY
            count_orders DESC;
        """
        return self.annotate(
            count_orders=Count('order')
        ).filter(
            count_orders__gt=2,
        ).order_by(
            '-count_orders'
        )