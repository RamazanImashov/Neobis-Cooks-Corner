BASE_SETTINGS = {
    "site_header": "Auth API",
    "site_brand": "Auth API",
    "welcome_sign": "Welcome to the library",
    "search_model": ["auth.User"],

    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
    ],
}