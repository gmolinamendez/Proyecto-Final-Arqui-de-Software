class EmailManager:
    def send_email(self, to_address, subject, body):
        print(f"Sending email to {to_address} with subject '{subject}'")
        return {
            "to_address": to_address,
            "subject": subject,
            "body": body,
            "status": "sent",
        }