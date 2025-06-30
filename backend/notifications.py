# backend/notifications.py
from dotenv import load_dotenv
load_dotenv()
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from routes_aoi import generate_thumbnail 

# Get your SendGrid API Key from your environment variables
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDER_EMAIL = "dhruvmali999@gmail.com" # Must be a verified sender in SendGrid

def send_change_alert_email(user_email: str, aoi_name: str, change_details: dict):
    if not SENDGRID_API_KEY:
        print("ERROR: SendGrid API Key not configured. Cannot send email.")
        return

    # Generate fresh URLs using the params stored in change_details
    before_url = generate_thumbnail(change_details["before_image_params"])
    after_url = generate_thumbnail(change_details["after_image_params"])

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=user_email,
        subject=f"Change Detected in your Area of Interest: {aoi_name}",
        html_content=f"""
        <h2>Alert: Significant Change Detected!</h2>
        <p>Our system has detected a significant change in your monitored Area of Interest (AOI): <strong>{aoi_name}</strong>.</p>
        <h3>Details:</h3>
        <ul>
            <li><strong>Type of Change Analyzed:</strong> Deforestation (NDVI Drop)</li>
            <li><strong>Area of Change:</strong> {change_details['area_of_change']:.2f} square meters.</li>
        </ul>
        <p>Please log in to the dashboard to review the changes.</p>
        <h3>Visual Comparison:</h3>
        <table style="width:100%;">
        <tr>
            <td style="text-align:center;"><strong>Before</strong></td>
            <td style="text-align:center;"><strong>After</strong></td>
        </tr>
        <tr>
            <td><img src="{before_url}" alt="Before Image" style="width:100%;"></td>
            <td><img src="{after_url}" alt="After Image" style="width:100%;"></td>
        </tr>
        </table>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Successfully sent alert email to {user_email}, Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")