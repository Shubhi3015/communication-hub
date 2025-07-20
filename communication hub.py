import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pywhatkit as kit
from twilio.rest import Client

st.set_page_config(page_title="Communication Hub", layout="centered")
st.title("📬 Communication Hub")

menu = st.sidebar.selectbox(
    "Choose a feature",
    ("Send Email", "Send WhatsApp Message", "Send SMS", "Make Phone Call")
)

if menu == "Send Email":
    st.header("📩 Send an Email via Gmail")

    sender_email = st.text_input("Your Gmail address")
    app_password = st.text_input("Your Gmail App Password", type="password")
    receiver_email = st.text_input("Recipient's Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message")

    if st.button("Send Email"):
        if not sender_email or not app_password or not receiver_email:
            st.error("Please fill in all required fields.")
        else:
            try:
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message.attach(MIMEText(body, "plain"))

                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(sender_email, app_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())

                st.success("✅ Email sent successfully!")

            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")

elif menu == "Send WhatsApp Message":
    st.header("💬 Send a WhatsApp Message")

    phone = st.text_input("Phone Number (with country code, e.g., +91XXXXXXXXXX)")
    message = st.text_area("Message")
    send_now = st.checkbox("Send instantly (wait ~10–20 sec)")

    if not send_now:
        col1, col2 = st.columns(2)
        hour = col1.number_input("Hour (24hr format)", min_value=0, max_value=23, value=12)
        minute = col2.number_input("Minute", min_value=0, max_value=59, value=0)

    if st.button("Send WhatsApp Message"):
        if not phone or not message:
            st.error("Please enter both phone number and message.")
        else:
            try:
                if send_now:
                    kit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)
                    st.success("✅ Message sent instantly! Keep your browser open.")
                else:
                    kit.sendwhatmsg(phone, message, int(hour), int(minute))
                    st.success(f"✅ Message scheduled at {hour:02d}:{minute:02d}. Keep the browser open.")
            except Exception as e:
                st.error(f"❌ Failed to send message: {e}")

elif menu == "Send SMS":
    st.header("📲 Send SMS via Twilio")

    account_sid = st.text_input("Twilio Account SID")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Your Twilio Phone Number (e.g. +1234567890)")
    recipient_number = st.text_input("Recipient's Phone Number (e.g. +91XXXXXXXXXX)")
    message_body = st.text_area("Message")

    if st.button("Send SMS"):
        if not account_sid or not auth_token or not twilio_number or not recipient_number or not message_body:
            st.error("Please fill in all fields.")
        else:
            try:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=message_body,
                    from_=twilio_number,
                    to=recipient_number
                )
                st.success(f"✅ SMS sent successfully! Message SID: {message.sid}")
            except Exception as e:
                st.error(f"❌ Failed to send SMS: {e}")

elif menu == "Make Phone Call":
    st.header("📞 Make a Phone Call via Twilio")

    account_sid = st.text_input("Twilio Account SID")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    twilio_number = st.text_input("Your Twilio Phone Number (e.g. +1234567890)")
    to_number = st.text_input("Recipient's Phone Number (e.g. +91XXXXXXXXXX)")
    message_text = st.text_area("Message to speak", "Hello, this is a test call from Streamlit!")

    if st.button("Make Call"):
        if not account_sid or not auth_token or not twilio_number or not to_number or not message_text:
            st.error("Please fill in all fields.")
        else:
            try:
                client = Client(account_sid, auth_token)
                twiml = f'<Response><Say>{message_text}</Say></Response>'
                call = client.calls.create(
                    to=to_number,
                    from_=twilio_number,
                    twiml=twiml
                )
                st.success(f"✅ Call initiated! Call SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Failed to make the call: {e}")
