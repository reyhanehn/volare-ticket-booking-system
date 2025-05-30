from django.db import models


class ReportType(models.TextChoices):
    RESERVATION = 'Reservation'
    PAYMENT = 'Payment'
    TICKET = 'Ticket'


class ReportStatus(models.TextChoices):
    PENDING = 'Pending'
    CHECKED = 'Checked'


class Report(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports_made'
    )
    admin = models.ForeignKey(
        'accounts.Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_handled'
    )
    status = models.CharField(
        max_length=10,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING
    )
    text = models.TextField(null=False)
    answer = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=15,
        choices=ReportType.choices,
        null=False
    )
    related_report = models.ForeignKey(
        'bookings.Ticket',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        # Enforce Account_ID != Admin_ID if both are set
        if self.account and self.admin and self.account_id == self.admin_id:
            raise ValidationError("Account and Admin cannot be the same.")
        # Enforce admin presence if status is Checked
        if self.status == ReportStatus.CHECKED and not self.admin:
            raise ValidationError("Admin must be assigned if report status is Checked.")

    def __str__(self):
        return f"Report {self.report_id} - {self.type} - {self.status}"
