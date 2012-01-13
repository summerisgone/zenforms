# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Card, Profile

class CardInline(admin.StackedInline):
    model = Card

class ProfileAdmin(admin.ModelAdmin):
   model = Profile
   inlines = [CardInline,]

admin.site.register(Card)
admin.site.register(Profile, ProfileAdmin)