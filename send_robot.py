import pandas as pd
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from premailer import transform

with open("latest_result.txt", "r") as f:
    csv_path = f.read().strip()
df = pd.read_csv(csv_path)

def format_status(status):
    s = str(status).strip().lower()
    if s == "completed":
        return '<span style="color: green; font-weight: bold;">COMPLETED</span>'
    elif s == "error":
        return '<span style="color: red; font-weight: bold;">ERROR</span>'
    elif s == "stopped":
        return '<span style="color: orange; font-weight: bold;">STOPPED</span>'
    else:
        return f'<span style="color: gray;">{status}</span>'

df["Status"] = df["Status"].apply(format_status)
df = df.fillna("N/A")

table_html = df.to_html(index=False, escape=False, border=1)

table_html = table_html.replace(
    '<table border="1" class="dataframe">',
    '''<table border="1" cellspacing="0" cellpadding="6" style="
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        font-size: 14px;
    ">'''
).replace(
    '<th>', '<th style="background-color:#2e6c80;color:white;text-align:left;">'
).replace(
    '<tr style="text-align: right;">', '<tr>'
)

with open("template.html", "r") as f:
    html_template = Template(f.read())

email_body = html_template.safe_substitute(table=table_html)

msg = MIMEMultipart("alternative")
msg["Subject"] = "Robot Test Report"
msg["From"] = "nguyenkimtrong43925@gmail.com"

recipients_to = ["nguyen.trong@kaonbroadband.com", "jungyu.choi@kaonbroadband.com"]
# recipients_cc = ["bob@example.com"]

msg["To"] = ", ".join(recipients_to)
# msg["Cc"] = ", ".join(recipients_cc)

msg.attach(MIMEText(email_body, "html"))

smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtp_server.login("nguyenkimtrong43925@gmail.com", "tvgmiggtjjrrzbsg")

# all_recipients = recipients_to + recipients_cc
all_recipients = recipients_to
smtp_server.sendmail(msg["From"], all_recipients, msg.as_string())

smtp_server.quit()
print("Email with styled HTML table sent to multiple recipients.")
