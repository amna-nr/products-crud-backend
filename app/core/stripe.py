from stripe import StripeClient
from app.core.config import settings


client = StripeClient(settings.STRIPE_SECRET_KEY)