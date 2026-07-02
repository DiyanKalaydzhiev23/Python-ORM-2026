from django.contrib import admin
from django_easy_query_builder.mixins import AdvancedSearchAdminMixin

from main_app.models import Car


@admin.register(Car)
class CarAdmin(AdvancedSearchAdminMixin, admin.ModelAdmin):
    list_display = ["model", "year", "owner", "car_details"]
    advanced_search_fields = [
        "model",
        "year",
        "registration__registration_number",
    ]

    def car_details(self, obj: Car):
        try:
            owner_name = obj.owner.name
        except AttributeError:
            owner_name = "No owner"

        try:
            plate = obj.registration.registration_number
        except AttributeError:
            plate = "No registration number"

        return f"Owner: {owner_name}, Registration: {plate}"

    car_details.short_description = "Car Details"
