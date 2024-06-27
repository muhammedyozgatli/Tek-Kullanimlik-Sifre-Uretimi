import pyotp
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox
import webbrowser
import threading
import time
class OTPVerificationApp:
    def __init__(self):

        self.otp = None
        self.remaining_time = 60 

        self.root = tk.Tk()
        self.root.title("TEK KULLANIMLIK ŞİFRE ÜRETİMİ VE UYGULAMALARI")
        self.root.geometry("600x400")  

       
        self.email_label = tk.Label(self.root, text="E-posta Adresi", font=("Arial", 12))
        self.email_label.grid(row=0, column=1, pady=10, padx=10) 

        self.email_entry = tk.Entry(self.root, font=("Arial", 12), width=35)  
        self.email_entry.grid(row=1, column=1, pady=10, padx=10)


        self.send_button = tk.Button(self.root, text="Gönder", command=self.send_otp, font=("Arial", 12), bg="green", fg="white")
        self.send_button.grid(row=2, column=1, pady=10, padx=10)


        self.otp_label = tk.Label(self.root, text="Tek Kullanımlık Şifre", font=("Arial", 12))
        self.otp_label.grid(row=6, column=1, pady=10, padx=10)

        self.countdown_label = tk.Label(self.root, text=" ".format(self.remaining_time), font=("Arial", 12))
        self.countdown_label.grid(row=2, column=2, pady=10, padx=10, sticky="e")

        self.otp_var = tk.StringVar()  
        self.otp_var.set("") 

        self.otp_entry = tk.Entry(self.root, font=("Arial", 12), width=30, show="*", textvariable=self.otp_var)  
        self.otp_entry.grid(row=7, column=1, pady=10, padx=10)

      
        self.show_password_checkbutton = tk.Checkbutton(self.root, text="Şifreyi Göster", command=self.show_password, font=("Arial", 12))
        self.show_password_checkbutton.grid(row=7, column=2, pady=10, padx=10)

       
        self.verify_button = tk.Button(self.root, text="Doğrula", command=self.verify_otp, font=("Arial", 12), bg="blue", fg="white")
        self.verify_button.grid(row=8, column=1, pady=10, padx=10)

    def generate_otp(self, secret_key):

        totp = pyotp.TOTP(secret_key, interval=60)
        otp = totp.now()
        return otp

    def send_email(self, sender_email, app_password, receiver_email, subject, body):
      
        try:
           
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

           
            server = smtplib.SMTP("smtp hostu girin", "port numaranız")
            server.starttls()

           
            server.login(sender_email, app_password)

           
            server.sendmail(sender_email, receiver_email, message.as_string())

          
            server.quit()

            messagebox.showinfo("Bilgi", "E-posta başarıyla gönderildi.")

        except Exception as e:
            messagebox.showerror("Hata", f"E-posta gönderme hatası:\n{str(e)}")

    def send_otp(self):
        sender_email = "gonderen mail"
        app_password = "sifreniz"
        receiver_email = self.email_entry.get()

     
        otp_secret_key = pyotp.random_base32()
        self.otp = self.generate_otp(otp_secret_key)
        subject = "Tek Kullanımlık Şifre"
        body = f"Giriş Şifreniz {self.otp} olarak oluşturulmuştur."

    
        self.send_email(sender_email, app_password, receiver_email, subject, body)

      
        self.start_countdown()

    def verify_otp(self):
        girdi = self.otp_entry.get()
        if girdi == self.otp and self.remaining_time > 0:
            messagebox.showinfo("Başarılı", "SAYFAYA YONLENDIRILIYORSUNUZ...")

          
            webbrowser.open("Gitmek istediğiniz URL")
        elif girdi == self.otp and self.remaining_time <= 0:
            messagebox.showinfo("Uyarı", "Üzgünüz, süreniz doldu. Yeni şifre alınız.")
        else:
            messagebox.showerror("Hata", "Doğrulama başarısız. Erişim Reddedildi...")

    def show_password(self):
       
        if self.otp_entry.cget("show") == "*":
            self.otp_entry.config(show="")
        else:
            self.otp_entry.config(show="*")

    def start_countdown(self):
       
        countdown_thread = threading.Thread(target=self.update_countdown)
        countdown_thread.start()

    def update_countdown(self):
        while self.remaining_time > 0:
            time.sleep(1) 
            self.remaining_time -= 1

            
            self.countdown_label.config(text="Şifrenin geçerli kalan süresi: {} saniye".format(self.remaining_time))

       
        self.countdown_label.config(text="Süre bitti yeni şifre alın!")

    def run(self):
        self.root.mainloop()


otp_app = OTPVerificationApp()
otp_app.run()
