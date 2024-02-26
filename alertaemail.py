import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()


def send_mail(body):

    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')
    email_cliente1 = os.getenv('EMAIL_CLIENTE1')

    contacts = [email_cliente1, "vilsonlopes@yahoo.com.br"]

    msg = EmailMessage()
    msg['Subject'] = "Imóveis Caixa"
    msg['From'] = email_address
    msg['To'] = ','.join(contacts)

    # The email body for recipients with non-HTML email clients.
    body_text = ""
    # The HTML body of the email.
    body_html = (f'<html><head><style>body {{color: #1f2a47;font-family: sans-serif;text-rendering: '
                 f'optimizelegibility;font-variant-ligatures: common-ligatures;}}.control-item {{float: '
                 f'left;margin-bottom: 0;padding-right: 1.5%;}}.control-span-12_12 {{width: 100%;}}.button-group,'
                 f'.control-group {{margin-bottom: 0;}}.button-group,.control-group {{display: table;margin-bottom: '
                 f'2em;}}.no-bullets,.scroll-nav ol,.scroll-nav ul {{list-style: none;padding: 0;margin: 0;}}.wrapper '
                 f'*,.wrapper ::before,.wrapper ::after {{-webkit-box-sizing: border-box;-moz-box-sizing: '
                 f'border-box;box-sizing: border-box;}}li {{ margin-bottom: .5em;}}.fotoimovel-col1 {{float: '
                 f'left;position: relative;padding: 5px 5px;width: 180px;height: auto;text-align: center; display: '
                 f'flex; align-items: center; justify-content: center; display: block;margin-left: auto;margin-right: '
                 f'auto;}}.fotoimovel {{max-width: 180px;max-height: 180px; icon: hand;}}img {{vertical-align: '
                 f'middle;}}img {{border: 0;}}.dadosimovel-col2 {{width: 70%;max-width: 70%;}}.dadosimovel-col2 {{'
                 f'float: left;position: relative;overflow: hidden;padding: 10px 15px;}}.form-set.inside-set {{width: '
                 f'100%;}}.legend,.legend-favoritos,.form-set {{float: left;}}.form-set {{opacity: 1;transition: '
                 f'opacity .3s ease-in;}}.no-bullets,.scroll-nav ol,.scroll-nav ul {{list-style: none;padding: '
                 f'0;margin: 0;}}.control-item {{float: left;margin-bottom: 0;padding-right: 1.5%;}}b,'
                 f'strong {{font-weight: bold;}}a {{border-bottom: 1px solid transparent;color: '
                 f'#006bae;text-decoration: none;-webkit-transition: color .2s, border-bottom-color '
                 f'.2s;-moz-transition: color .2s, border-bottom-color .2s;transition: color .2s, border-bottom-color '
                 f'.2s;}}:last-child.form-row {{margin-bottom: 0px;}}</style></head><body>{body}</body></html>')

    msg.set_content(body_html)
    # msg.add_alternative(body_text, subtype='text')
    msg.add_alternative(body_html, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(email_address, email_password)
            server.send_message(msg)
    except Exception as e:
        print(f'Erro ao enviar {e}')
    else:
        print('Email enviado com sucesso!')
