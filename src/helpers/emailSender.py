import smtplib
import email.message
import os

def send_email_reset_password(emailClient, name, password):
    body = f"""
    <h1>Olá, {name}</h1>
    <p>Seu pedido de redefinição de senha foi realizado com sucesso.</p>
    <p>Sua senha temporária é: {password}</p>
    <a href="http://klote.netlify.app">Clique para fazer login</a>
    """.encode('utf-8')
    msg = email.message.EmailMessage()
    msg['Subject'] = 'KLOTE: Redefinição de senha'
    msg['From'] = os.getenv("EMAIL")
    msg['To'] = emailClient
    password = os.getenv("PASSWORD_EMAIL")
    
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.send_message(msg)
    s.quit()

def send_email_new_guest(emailClient, name, password):
    body = f"""
    <h1>Olá, {name}</h1>
    <p>Seu cadastro foi realizado com sucesso.</p>
    <p>Para acessar o sistema, utilize os dados abaixo:</p>
    <p>E-mail: {emailClient}</p>
    <p>Senha: {password} </p>
    <p>A senha é temporária, você pode alterá-la após o primeiro login.</p>
    <p>Para acessar o sistema, clique no link abaixo:</p>
    <a href="http://klote.netlify.app">Acessar sistema</a>
    """.encode('utf-8')
    msg = email.message.EmailMessage()
    msg['Subject'] = 'KLOTE: Cadastro realizado'
    msg['From'] = os.getenv("EMAIL")
    msg['To'] = emailClient
    password = os.getenv("PASSWORD_EMAIL")
    
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(body)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.send_message(msg)
    s.quit()