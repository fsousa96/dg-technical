import requests
import base64

def list_tickets():

    url = "https://{your host here}.gorgias.com/api/tickets?limit=30&order_by=created_datetime%3Adesc"

    # Set up the API authentication credentials and build header
    headers = build_headers("your email here","your api token here")

    response = requests.get(url, headers=headers)

    print(response.text)

def build_headers(email,api_token):
    """
    Set up the API authentication (base64 encoding) credentials and build header
    Args:
        agent_email (str): The email address of the agent account used to authenticate in Gorgias.
        email_text (str): The text of the email we are sending.
    Returns:
        json: Headers
    """

    userpass = f"{email}" + ':' + f"{api_token}"
    encoded_u = base64.b64encode(userpass.encode()).decode()

    headers = {
        "accept": "application/json",
        "authorization": "Basic %s" % encoded_u
    }

    return headers

def build_payload(user_email, email_text, channel):
    """
    Constructs the JSON payload for the new email reply.
    Args:
        user_email (str): The email address of the agent user on whose behalf we are sending the response.
        email_text (str): The text of the email we are sending.
        channel (str): The channel on which to send the reply (email or internal-note).
    Returns:
        json: Payload
    """

    payload = {
        "receiver": {"email": "receiver email here"},
        "source": {
            "to": [
                {
                    "name": "Francisco Sousa",
                    "address": "receiver email here"
                }
            ],
            "from": {"address": f"{user_email}"},
            "type": f"{channel}"
        },
        "body_html": f"{email_text}",
        "body_text": f"{email_text}",
        "channel": f"{channel}",
        "from_agent": True,
        "via": "api"
    }

    return payload

def send_reply(ticket_id, user_email, email_text, api_token, channel="email"):
    """
    Sends a new email reply on the specified ticket using the Gorgias REST API.
    Args:
        ticket_id (int): The ID of the ticket on which to send the reply.
        user_email (str): The email address of the agent user on whose behalf we are sending the response.
        email_text (str): The text of the email we are sending.
        api_token (str): The API token used to authenticate with the Gorgias API.
        channel (str): The channel on which to send the reply (email or internal-note). Default is email.
    Returns:
        bool: True if the email reply was sent successfully, False otherwise.
    """

    # Set up the API endpoint URL.
    url = f"https://{your host here}.gorgias.com/api/tickets/{ticket_id}/messages"

    # Set up the API authentication credentials and build header
    headers = build_headers("you email here",api_token)
    
    # Construct the JSON payload for the new email reply.
    payload = build_payload(user_email, email_text, channel)

    # Send the API request to create the new email reply on the ticket.
    response = requests.post(url, headers=headers, json=payload)

    # Handle any errors or exceptions that may occur.
    if response.status_code == 201:
        print(f"New reply sent via {channel}")
        return True
    else:
        print(f"Error sending new email reply: {response.text}")
        return False
    
def main():
    # SET VARIABLES 
    ticket_id = "ticket id here"
    user_email = "sender email here" 
    api_token="your api token here"

    # WRITE EMAIL MESSAGE HERE
    email_text = '''This is an example message sent to my email'''

    send_reply(ticket_id, user_email, email_text, api_token)

    # WRITE INTERNAL MESSAGE HERE
    internal_text = '''This is an example message sent as an Internal Note'''

    send_reply(ticket_id, user_email, internal_text, api_token, "internal-note")

if __name__ == "__main__":
    main()