import requests
from django.core.mail import EmailMultiAlternatives, get_connection
connection = None
def set_connection(config):
    global connection
    try:
        if not connection:
            connection = get_connection(
                backend='django_smtp_ssl.SSLEmailBackend',
                host=config.smtp_host,
                port=config.smtp_port,
                username=config.smtp_username,
                password=config.smtp_password, 
                use_tls=config.smtp_SSL,
            )
    except Exception as e:
        print(e)
def send(order,recivers:list[str]=[],config=None):
    set_connection(config)
    send_by_telegram(order,recivers,config)
    send_by_mail(order,config)
def order_to_message(order):
    return 'testing'
def order_to_html(order):
    return 'aaa','bbb','ccc'
def send_by_telegram(order,recivers:list[str]=[],config=None):
    recivers.extend(config.get_telegram_recivers())
    message=order_to_message(order)
    bot_api = f'https://api.telegram.org/bot{config.telegram_bot_api}/sendMessage' if config else ' '
    for seciver in recivers:
        try:
            requests.post(bot_api, json={'chat_id': seciver, 'text': message})
        except Exception as e:
            print(e)
def send_by_mail(order,config=None):
    bcc=config.get_email_recivers()
    subject, message, html_message=order_to_html(order)
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=config.smtp_username,
            to=[order.email],
            bcc=bcc,
            connection=connection
        )
        msg.content_subtype = "html"
        msg.attach_alternative(html_message, "text/html")
        msg.send()
    except Exception as e:
        print(e)