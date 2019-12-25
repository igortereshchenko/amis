import smtplib
from email.mime.text import MIMEText


def send_email(Answer_for_question, Questions, Student_answer, User_faculty, User_email):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = 'd9928e9abaf875'
    password = 'd7ac289367d297'
    message = f"<h3>Answer(s) for question(s)</h3><ul><li>Student: {Student_answer}</li>" \
              f"<li>Faculty: {User_faculty} </li><li>Question: {Questions}</li>" \
              f"<li>Answer: {Answer_for_question}</li></ul>"

    sender_email = 'support@kpi.ua'
    receiver_email = f"{User_email}"
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Answer reply'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
