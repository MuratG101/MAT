import pytesseract
from PIL import Image
import re, csv, sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Tesseract-Pfad
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def bild_zu_tabelle(path):
    img = Image.open(path)
    text = pytesseract.image_to_string(img, lang='deu')
    if not text.strip(): raise ValueError("Keine Texte erkannt")
    data=[]
    for line in text.splitlines():
        m = re.match(r"^(\d+)\s+(\w+)\s+(.*?)\s+(\d+(?:×|x)\d+|\d+)", line)
        if not m: continue
        menge,name,rest,dim = m.groups()
        size_m = re.search(r"(\d+\s*(?:m|cm))", rest)
        size = size_m.group(1) if size_m else ""
        typ = rest.replace(size, '').strip()
        data.append([menge,name,typ,dim.replace('x','×'),size])
    return data

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("mAT – Material Analyse Tool")
        self.geometry("550x300")
        ttk.Label(self, text="Liste-Bild auswählen:", font=("Arial",13)).pack(pady=20)
        ttk.Button(self, text="Bild auswählen", command=self.load).pack()
    def load(self):
        path = filedialog.askopenfilename(filetypes=[("Bilder","*.png;*.jpg;*.jpeg")])
        if not path: return
        try:
            rows = bild_zu_tabelle(path)
            save = filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','.csv')])
            if save:
                with open(save,'w',newline='',encoding='utf-8') as f:
                    writer=csv.writer(f)
                    writer.writerow(["Menge","Material","Typ","Dimension","Größe"])
                    writer.writerows(rows)
                messagebox.showinfo('Erfolg',f'CSV gespeichert: {save}')
        except Exception as e:
            messagebox.showerror('Fehler',str(e))

if __name__=='__main__': App().mainloop()