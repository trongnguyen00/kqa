import pandas as pd
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from premailer import transform

# Đọc dữ liệu test từ file CSV/json (ví dụ sau dùng CSV)
with open("latest_result.txt", "r") as f:
    csv_path = f.read().strip()
df = pd.read_csv(csv_path)  # hoặc pd.read_json(...)

def format_status(status):
    s = str(status).strip().lower()
    if s == "pass":
        return '<span style="color: green; font-weight: bold;">PASS</span>'
    elif s == "fail":
        return '<span style="color: red; font-weight: bold;">FAIL</span>'
    elif s == "stopped":
        return '<span style="color: orange; font-weight: bold;">STOPPED</span>'
    else:
        return f'<span style="color: gray;">{status}</span>'
df["Status"] = df["Status"].apply(format_status)
df = df.fillna("N/A")
# Convert DataFrame thành bảng HTML

table_html = df.to_html(index=False, escape=False, border=1)

# Chèn style trực tiếp vào bảng
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


# Đọc template và thay thế
with open("template.html", "r") as f:
    html_template = Template(f.read())

email_body = html_template.safe_substitute(table=table_html)
# Soạn và gửi email
msg = MIMEMultipart("alternative")
msg["Subject"] = "Robot Test Report"
msg["From"] = "nguyenkimtrong43925@gmail.com"
msg["To"] = "nguyen.trong@kaonbroadband.com"
msg.attach(MIMEText(email_body, "html"))

# Gửi email qua Gmail
smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
smtp_server.login("nguyenkimtrong43925@gmail.com", "tvgmiggtjjrrzbsg")
smtp_server.send_message(msg)
smtp_server.quit()

print("✅ Email with styled HTML table sent.")
