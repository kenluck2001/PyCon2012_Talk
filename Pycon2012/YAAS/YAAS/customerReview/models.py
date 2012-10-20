from django.db import models
from datetime import datetime


class ProductReview(models.Model):
    STATUS_CHOICES = (
		(0, 'No Review'),
		(1, 'Worst'),
		(2, 'Very bad'),
		(3, 'Fair'),
		(4, 'Good'),
		(5, 'Best'),
	)
    rating = models.IntegerField(max_length=1, choices=STATUS_CHOICES, default=0)
    comment = models.CharField(max_length=80)
    created_at = models.DateTimeField(default=datetime.now(),blank=True, editable=False)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if ProductReview.objects.count() > 1:
            return

        super(ProductReview, self).save(*args, **kwargs)


