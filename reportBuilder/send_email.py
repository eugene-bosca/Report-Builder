import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def build_and_send_email(pr_data, general_data, email_list):
    sendgrid_api_token = os.getenv('SENDGRID_API_TOKEN')

    # Build the email and send through sendgrid
    message = Mail(
        from_email='eugene@codebusters.ca',
        to_emails=email_list,
        subject='Sending with Twilio SendGrid using Custom Template'
    )

    message.template_id = 'd-599d1adedbf145709f28557bce38bf08'

    message.dynamic_template_data = {
        "general_data": general_data,
        "pr_data": pr_data,
    }

    # Error handling
    try:
        sg = SendGridAPIClient(sendgrid_api_token)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print('Error:', str(e))
        print('Message not sent')