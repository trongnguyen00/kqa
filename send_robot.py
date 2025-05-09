import pandas as pd
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Đọc dữ liệu test từ file CSV/json (ví dụ sau dùng CSV)
df = pd.read_csv("/home/ats/ATS/kqa/result_20250509_182447.csv")  # hoặc pd.read_json(...)

# Optional: định dạng cột Status
# df['Status'] = df['Status'].apply(lambda x: f'<span class="pass">{x}</span>' if x == 'PASS' else f'<span class="fail">{x}</span>')

# Convert DataFrame thành bảng HTML
table_html = df.to_html(index=False, escape=False, classes="test-table")

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
