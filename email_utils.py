import resend
import os

resend.api_key = os.environ.get("RESEND_API_KEY")

def send_download_email(buyer_email):
    # 發送下載連結與 LINE 群組的郵件
    params = {
        "from": "Nexus Academy <noreply@nexus-academy.ai>",
        "to": [buyer_email],
        "subject": "🔓 您的 30 單字體驗權限已開通！",
        "html": """
            <h1>歡迎加入啟源學院！</h1>
            <p>親愛的學霸，您請求的體驗版已經準備就緒。</p>
            <p><a href="https://nexus-academy.ai/game">點此開始您的 SRS 高效記憶挑戰</a></p>
            <br>
            <p>為了獲取每日學測技巧，請務必加入我們的 LINE 社群：</p>
            <p><a href="https://line.me/ti/g2/qtxRWaF9DrdSsqv1_Is9ADWz78p-v39FYCAYcw">加入 LINE 社群</a></p>
            <p>祝 學習愉快！</p>
        """
    }
    try:
        resend.Emails.send(params)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
