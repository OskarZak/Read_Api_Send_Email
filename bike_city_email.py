import requests
import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage
import os
#ang, wybieranie kraju z którego jest uzytkownik, do CSV, wysylka mailem, ######requests
save_file = open('citybike_dtf.csv', 'wt', encoding= 'utf-8')

def main():
    

    url = 'http://api.citybik.es/v2/networks'
    data = requests.get(url).json()
    recipients = { "PL" : "oskarzak1999@gmail.com", "RU" : "patka379@onet.pl"  }
    for country in recipients:
        size = (len(data['networks']))
        list = []
        number = 0
        while number < size:
            if country == data['networks'][number]['location']['country']:
                list.append(data['networks'][number]['location'])
            number +=1
        
        df_b = pd.DataFrame(list)
        print(df_b)
        print("operacja 1 zostala zakonczona")
        class DailyDigestEmail:
            def __init__(self):
                self.content = {"tabela": {"include": True, "content": str(df_b)}}

                self.recipients_list = [recipients[country]] #lista odbiorcow

                self.sender_credentials = {'email': 'oskarzak1999@outlook.com', # mail z ktorego bedzie wysylane
                                        'password': 'Jestembogiem668!'} # haslo do maila

            def send_email(self):
        
                msg = EmailMessage()
                msg['Subject'] = f'Bike parks in your area - {datetime.date.today().strftime("%d %b %Y")}'
                msg['From'] = self.sender_credentials['email']
                msg['To'] = ', '.join(self.recipients_list)


                msg_body = self.format_message()
                msg.set_content(msg_body['text'])

                with smtplib.SMTP('smtp.office365.com', 587) as server:
                    server.starttls()
                    server.login(self.sender_credentials['email'],
                                self.sender_credentials['password'])
                    server.send_message(msg)


            def format_message(self):
                text = f'*~*~*~*~*~*~*~*~*~ Bike Parks In Your Area - {datetime.date.today().strftime("%d %b %Y")}*~*~*~*~*~*~*~*~*~\n\n'

                if self.content["tabela"]["include"]:
                    text+= 'You can find your parks here\n\n'
                    text += f'"{self.content["tabela"]["content"]}"\n\n'

                return {'text': text}

        if __name__ == "__main__":
            PASSWORD = os.environ.get('PASS')
            email = DailyDigestEmail()

            print("\nEmail body generation...")
            message = email.format_message()
            print("\nPlaintext email body is...")
            print(message["text"])

            with open('message_text.txt', 'w', encoding='utf-8') as f:
                f.write(message['text'])

            print("\nSending email...")
            email.send_email()

main()