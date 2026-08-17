TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # <-- BUNU EKLE
        'APP_DIRS': True,
        ...
    },
]

STATICFILES_DIRS = [BASE_DIR / 'static']    # <-- BUNU EKLE
STATIC_URL = '/static/'