RESOURCE = "https://graph.microsoft.com"  # Add the resource you want the access token for
TENANT = "b9bf37b6-dec0-40ae-9479-2fdd03b13252"  # Enter tenant name, e.g. contoso.onmicrosoft.com
AUTHORITY_HOST_URL = "https://login.microsoftonline.com"
CLIENT_ID = "88bbbd23-583b-4d24-b6b1-2fc0e5b28d10"  # copy the Application ID of your app from your Azure portal
CLIENT_SECRET = "gcaBKJJ81-(@rvybGIL343!"  # copy the value of key you generated when setting up the application
# These settings are for the Microsoft Graph API Call
API_VERSION = 'v1.0'
SCOPES = ['User.Read']  # Add other scopes/permissions as needed.
# This scope allows users to sign-in to the app, and allows the app to read the profile of signed-in users.
# It also allows the app to read basic company information of signed-in users.
# List of scopes/permissions - https://developer.microsoft.com/en-us/graph/docs/concepts/permissions_reference
