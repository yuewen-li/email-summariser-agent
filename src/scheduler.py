import schedule
import time
from datetime import datetime
from config.settings import DAILY_RUN_TIME, MAX_EMAILS_PER_DAY, SENDER_EMAIL
from src.email_client import OutlookClient
from src.summarizer import EmailSummarizer

class NewsletterScheduler:
    def __init__(self):
        self.email_client = OutlookClient()
        self.summarizer = EmailSummarizer()

    def process_newsletters(self):
        """Process newsletters and send daily brief"""
        try:
            # Fetch newsletters
            newsletters = self.email_client.fetch_newsletters()
            
            if not newsletters:
                print(f"No newsletters found at {datetime.now()}")
                return

            # Limit the number of emails to process
            newsletters = newsletters[:MAX_EMAILS_PER_DAY]
            
            # Process each newsletter
            summaries = []
            for newsletter in newsletters:
                summary = self.summarizer.summarize_email(
                    newsletter['subject'],
                    newsletter['body']['content']
                )
                
                summaries.append({
                    'subject': newsletter['subject'],
                    'summary': summary,
                    'sender': newsletter['from']['emailAddress']['address']
                })

            # Generate and send daily brief
            daily_brief = self.summarizer.generate_daily_brief(summaries)
            self.email_client.send_email(
                subject=f"📰 Daily Newsletter Brief - {datetime.now().strftime('%Y-%m-%d')}",
                body=daily_brief,
                recipient=SENDER_EMAIL
            )
            
            print(f"Successfully processed {len(summaries)} newsletters at {datetime.now()}")
            
        except Exception as e:
            print(f"Error processing newsletters: {str(e)}")

    def start(self):
        """Start the scheduler"""
        print(f"Starting newsletter scheduler. Will run daily at {DAILY_RUN_TIME}")
        schedule.every().day.at(DAILY_RUN_TIME).do(self.process_newsletters)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute 
