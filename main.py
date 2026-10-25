from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import base64
import hashlib

window = Tk()
window.title("TopSecret")
window.minsize(400, 700)
window.config(padx=20, pady=20)
window.columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Görsel Ekleme
raw_image = Image.open("topsecret.png")
resized_image = raw_image.resize((200, 200))
logo_img = ImageTk.PhotoImage(resized_image)

logo_label = Label(window, image=logo_img)
logo_label.image = logo_img
logo_label.grid(row=1, column=0, pady=10)

# Şifreleme Fonksiyonları
def generate_key(master_key):
    digest = hashlib.sha256(master_key.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def save_and_encrypt():
    title = my_entry.get()
    message = my_text.get("1.0", "end-1c")
    master_key = my_entry3.get()

    if len(title) == 0 or len(message) == 0 or len(master_key) == 0:
        messagebox.showwarning(title="Hata", message="Lütfen tüm alanları doldurun.")
        return

    try:
        key = generate_key(master_key)
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(message.encode())

        with open("my_secrets.txt", "a") as data_file:
            data_file.write(f"\n{title}\n{encrypted_message.decode()}\n")

        my_entry.delete(0, END)
        my_text.delete("1.0", END)
        my_entry3.delete(0, END)
        messagebox.showinfo(title="Başarılı", message="Notunuz şifrelenip dosyaya kaydedildi.")
    except Exception:
        messagebox.showerror(title="Hata", message="Şifreleme başarısız oldu!")

def decrypt_note():
    encrypted_message = my_text.get("1.0", "end-1c")
    master_key = my_entry3.get()

    if len(encrypted_message) == 0 or len(master_key) == 0:
        messagebox.showwarning(title="Hata", message="Lütfen şifreli metni ve anahtarı girin!")
        return

    try:
        key = generate_key(master_key)
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(encrypted_message.encode())

        my_text.delete("1.0", END)
        my_text.insert("1.0", decrypted_message.decode())
    except Exception:
        messagebox.showerror(title="Hata", message="Yanlış anahtar girdiniz veya metin hatalı!")


# Şifre Göster/Gizle Fonksiyonu
def toggle_password():
    if my_entry3.cget("show") == "*":
        my_entry3.config(show="")
        toggle_btn.config(text="🔒") # Gizlemek için kilit ikonu
    else:
        my_entry3.config(show="*")
        toggle_btn.config(text="👁") # Göstermek için göz ikonu


# Arayüz
my_label = Label(text="Enter your Title", font=("Times New Roman", 15))
my_label.grid(row=4, column=0)

my_entry = Entry(width=40)
my_entry.grid(row=5, column=0)

my_label2 = Label(text="Enter your Secret", font=("Times New Roman", 15))
my_label2.grid(row=6, column=0, pady=(20,0))

my_text = Text(width=40, height=20)
my_text.grid(row=7, column=0, pady=(0,20))

my_label3 = Label(text="Enter Master Key", font=("Times New Roman", 15))
my_label3.grid(row=8, column=0)

# İç içe görünüm (Frame ile Tek Kutu Görünümü)
# 1. Çerçeveyi sanki bir giriş kutusuymuş gibi kenarlıklı (sunken) ve beyaz yapıyoruz
password_frame = Frame(window, bg="white", bd=2, relief="sunken")
password_frame.grid(row=9, column=0, pady=(0,10))

# 2. Giriş kutusunun kendi kenarlığını (bd=0) tamamen siliyoruz
my_entry3 = Entry(password_frame, width=35, show="*", bd=0, highlightthickness=0)
my_entry3.grid(row=0, column=0, ipady=3, padx=2)

# 3. Butonun arka planını beyaz, kenarlığını 0 yapıyoruz (kutunun parçası gibi duruyor)
# cursor="hand2" parametresi, farenin buton üzerine gelince el işaretine dönmesini sağlıyor.
toggle_btn = Button(password_frame, text="👁", bd=0, bg="white", cursor="hand2", command=toggle_password)
toggle_btn.grid(row=0, column=1, padx=(2, 5))
# -----------------------------------------------------------

my_button = Button(text="Save & Encrypt", command=save_and_encrypt)
my_button.grid(row=10, column=0, pady=(0,3))

my_button2 = Button(text="Decrypt", command=decrypt_note)
my_button2.grid(row=11, column=0)

window.mainloop()