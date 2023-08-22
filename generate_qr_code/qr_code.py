import pyqrcode

def generate_whatsapp_message_url(number, message, full_msg=None):
    url = f"https://wa.me/{number}?text={message}"
    if full_msg:
        url = full_msg
    return url


def create_qr_code(url, file_name):
    qr_code = pyqrcode.create(url)
    qr_code.png(file_name, scale=8)

whatsapp_number = "+33617705677"  # Replace with the desired WhatsApp number
initial_message = "Yes, I would love to subscribe to more news :) "  # Replace with your initial message

# #  general 
# qr_code_file = "whatsapp_qrcode_general.png"  # Specify the file name and extension
# message_url = generate_whatsapp_message_url(whatsapp_number, "This is a demo for general informations about Krispy.")
# create_qr_code(message_url, qr_code_file)

# # marketing
# qr_code_file = "whatsapp_qrcode_marketing.png"  # Specify the file name and extension
# message_url = generate_whatsapp_message_url(whatsapp_number, "This is a demo for markting.")
# create_qr_code(message_url, qr_code_file)


# # feedback
# qr_code_file = "whatsapp_qrcode_feedback.png"  # Specify the file name and extension
# message_url = generate_whatsapp_message_url(whatsapp_number, "This is a demo for feedback.")
# create_qr_code(message_url, qr_code_file)


# krispy
qr_code_file = "whatsapp_the_skin.png"  # Specify the file name and extension
message_url = generate_whatsapp_message_url(whatsapp_number, "Please send this first message as is to start a conversation...")
create_qr_code(message_url, qr_code_file)