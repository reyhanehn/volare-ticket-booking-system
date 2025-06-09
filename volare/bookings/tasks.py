from celery import shared_task

@shared_task
def cancel_expired_reservations():
    from django.utils import timezone
    from .models import Reservation, ReservationStatus

    now = timezone.now()

    # Filter reservations that are pending and expired (expiration_time <= now)
    expired = Reservation.objects.filter(
        status=ReservationStatus.PENDING,
        expiration_time__lte=now
    )

    count = expired.count()
    expired.update(status=ReservationStatus.CANCELLED)

    return f"Cancelled {count} expired reservations"
