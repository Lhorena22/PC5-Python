import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def enviar_correo(destinatario, asunto, mensaje, archivo_adjunto=None):
    servidor_smtp = 'smtp.gmail.com'
    puerto = 587
    remitente = ''
    contraseña = ''

    msg = MIMEMultipart()

    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    msg.attach(MIMEText(mensaje, 'plain'))

    if archivo_adjunto:
        adjunto = open(archivo_adjunto, 'rb')
        parte_adjunta = MIMEBase('application', 'octet-stream')
        parte_adjunta.set_payload((adjunto).read())
        encoders.encode_base64(parte_adjunta)
        parte_adjunta.add_header('Content-Disposition', "attachment; filename= %s" % archivo_adjunto)
        msg.attach(parte_adjunta)

    servidor = smtplib.SMTP(servidor_smtp, puerto)
    servidor.starttls()
    servidor.login(remitente, contraseña)

    servidor.sendmail(remitente, destinatario, msg.as_string())

    servidor.quit()

if __name__ == "__main__":

    enviar_correo('destinatario@gmail.com', 'Prueba de correo', 'Este es un correo de prueba desde Python', 'archivo_adjunto.txt')
