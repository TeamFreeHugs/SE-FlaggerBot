#IMPORTANT
[Please visit this link](https://stackexchange.com/oauth/dialog?client_id=5583&scope=write_access,no_expiry&redirect_uri=https://stackexchange.com/oauth/login_success), then approve it.
Copy the `#access_token=` hash from the redirect
After that, create a file `api_details.py` and add this:

    token = '<access token here>'