import resend
from langchain_core.tools import tool
from .config import config

smtp_config = config.get("send_email", {})
resend_api_key = smtp_config.get("resend_api_key")
from_email = smtp_config.get("from_email")


@tool(parse_docstring=True)
def send_email(email: str, subject: str, content: str) -> str:
    """Send emails

    Args:
        email (str): Email address of the recipient
        subject (str): Email subject
        content (str): Email body content
    """
    try:
        resend.api_key = resend_api_key
        
        to_emails = email if isinstance(email, list) else [email]
        
        params = {
            "from": from_email,
            "to": to_emails,
            "subject": subject,
            "text": content,
        }
        
        response = resend.Emails.send(params)
        print("邮件发送成功!")
        return response
        
    except Exception as e:
        print(f"邮件发送失败: {e}")
        return None

tools = [send_email]