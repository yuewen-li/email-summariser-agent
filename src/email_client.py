import msal
import requests
from datetime import datetime, timedelta
from config.settings import (
    OUTLOOK_CLIENT_ID,
    NEWSLETTER_FILTERS,
)

class OutlookClient:
    def __init__(self):
        self.access_token = None
        self.graph_url = "https://graph.microsoft.com/v1.0"
        self.app = msal.PublicClientApplication(
            OUTLOOK_CLIENT_ID,
            authority="https://login.microsoftonline.com/consumers"  # Use consumers authority for personal accounts
        )
        
    def get_access_token(self):
        """Get access token using interactive authentication"""
        scopes = ["User.Read", "Mail.Read", "Mail.Send"]
        
        # Try to get token from cache first
        accounts = self.app.get_accounts()
        if accounts:
            result = self.app.acquire_token_silent(scopes, account=accounts[0])
        else:
            result = None
            
        if not result:
            # No suitable token in cache, get a new one via interactive sign in
            result = self.app.acquire_token_interactive(scopes)
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            print("Successfully obtained access token")
            return True
        else:
            print(f"Failed to get access token: {result.get('error_description')}")
            return False

    def get_headers(self):
        """Get headers for API requests"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def fetch_newsletters(self, hours=24):
        """Fetch newsletters from the last 24 hours"""
        if not self.access_token and not self.get_access_token():
            raise Exception("Failed to get access token")

        # Calculate time range
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)
        
        # Build filter query for senders
        sender_conditions = []
        for sender_filter in NEWSLETTER_FILTERS:
            if '@' in sender_filter:
                # Exact email match
                sender_conditions.append(f"from/emailAddress/address eq '{sender_filter}'")
            else:
                # Domain match
                sender_conditions.append(f"endswith(from/emailAddress/address,'{sender_filter}')")
        
        # Combine time filter with sender filter
        filter_query = f"receivedDateTime ge {start_time.isoformat()}Z"
        if sender_conditions:
            filter_query += f" and ({' or '.join(sender_conditions)})"
        
        # Make API request
        response = requests.get(
            f"{self.graph_url}/me/messages",
            headers=self.get_headers(),
            params={
                '$filter': filter_query,
                '$select': 'subject,body,from,receivedDateTime',
                '$orderby': 'receivedDateTime desc'
            }
        )
        
        if response.status_code == 200:
            return response.json().get('value', [])
        else:
            raise Exception(f"Failed to fetch emails: {response.text}")

    def send_email(self, subject, body, recipient):
        """Send email using Microsoft Graph API"""
        if not self.access_token and not self.get_access_token():
            raise Exception("Failed to get access token")

        email_data = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'HTML',
                    'content': body
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': recipient
                        }
                    }
                ]
            }
        }

        # Use /me endpoint for delegated permissions
        response = requests.post(
            f"{self.graph_url}/me/sendMail",
            headers=self.get_headers(),
            json=email_data
        )

        if response.status_code != 202:
            raise Exception(f"Failed to send email: {response.text}")

if __name__ == "__main__":
    outlook_client = OutlookClient()
    newletters = outlook_client.fetch_newsletters()
    print(newletters)