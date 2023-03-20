import requests
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async

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
def send(order,recivers:list[str]=[],config=None,request=None):
    set_connection(config)
    send_by_telegram(order,recivers,config)
    send_by_mail(order,config,request)
def order_to_message(order,config):
    message=f"======={order.date_ordered.strftime('%d-%m-%Y %H:%M:%S')}======\n"
    message+=f"id: #{order.id}\n"
    message+=f"name: {order.name}\n"
    message+=f"token: {order.token}\n" if order.token else ''
    message+=f"email: {order.email}\n" if order.email else ''
    message+=f"phone: {order.phone}\n"
    message+=f"address: {order.address}\n"
    message+=f"city: {order.city}\n\n"
    for item in order.items.all():
        message+=f"{item.quantity} x {item.product.name}\n"
        message+=f"type: {item.product.category.name}\n"
        for p in item.properties.all():  message+=f" {p.name},"
        message+=f" {item.total_price} {config.currency.code}\n\n"
    message+=f"\n"
    message+=f"payment_method: {order.payment_method}\n"
    message+=f"total_price: {order.total_price} {config.currency.code}\n"
    message+=f"==============================\n"
    return message
def order_to_html(order,config,request):
    subject='('+order.date_ordered.strftime('%d-%m-%Y %H:%M:%S')+') New Order: '+str(order.id)+' '+order.name
    message='Order Confirmed'
    html=render_to_string('email/order.html',{'config':config,'order':order},request=request)
    return subject,message,html
async def send_by_telegram(order,recivers:list[str]=[],config=None):
    recivers.extend(config.get_telegram_recivers())
    message=order_to_message(order,config)
    bot_api = f'https://api.telegram.org/bot{config.telegram_bot_api}/sendMessage' if config else ' '
    for seciver in recivers:
        try:
            await sync_to_async(requests.post(bot_api, json={'chat_id': seciver, 'text': message}), thread_sensitive=False)
        except Exception as e:
            print(e)
async def send_by_mail(order,config=None,request=None):
    bcc=config.get_email_recivers()
    subject, message, html_message=order_to_html(order,config,request)
    recivers=[order.email] if order.email else bcc
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=config.smtp_username,
            to=recivers,
            bcc=bcc if not order.email else [],
            connection=connection
        )
        msg.content_subtype = "html"
        msg.attach_alternative(html_message, "text/html")
        await sync_to_async(msg.send(), thread_sensitive=False)
    except Exception as e:
        print(e)