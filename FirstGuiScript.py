import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import json
import os

# Datei zum Speichern der Einträge
entries_file = "entries.json"

# Funktion zum Laden der Einträge aus der JSON-Datei
def load_entries():
    if os.path.exists(entries_file):
        with open(entries_file, "r") as f:
            return json.load(f)
    return []

# Funktion zum Speichern der Einträge in die JSON-Datei
def save_entries():
    with open(entries_file, "w") as f:
        json.dump(entries, f)

# Funktion, die ausgeführt wird, wenn ein Knopf gedrückt wird
def button_click(button_number):
    if button_number == 1:
        open_text_window()
    elif button_number == 2:
        upload_file("image")
    elif button_number == 3:
        upload_file("pdf")
    else:
        print(f"Button {button_number} clicked!")

# Funktion zum Öffnen eines neuen Fensters zur Texteingabe
def open_text_window():
    def save_text():
        # Text aus dem Textfeld holen und speichern
        entered_text = text_entry.get("1.0", tk.END).strip()
        if entered_text:
            entries.append({'type': 'text', 'content': entered_text})
            save_entries()
            update_display()
        # Fenster schließen
        text_window.destroy()

    def cancel():
        # Fenster ohne Speichern schließen
        text_window.destroy()

    # Neues Fenster für die Texteingabe erstellen
    text_window = tk.Toplevel(root)
    text_window.title("Text Eingeben")
    text_window.geometry("400x300")
    text_window.configure(bg="#2c3e50")

    # Textfeld für die Eingabe erstellen
    text_entry = tk.Text(text_window, wrap=tk.WORD, height=10, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 12))
    text_entry.pack(expand=True, fill=tk.BOTH, padx=10, pady=(10, 0))
    text_entry.focus_set()

    # Rahmen für die Buttons erstellen
    button_frame = tk.Frame(text_window, bg="#2c3e50")
    button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    # Speichern-Button erstellen
    save_button = tk.Button(button_frame, text="Speichern", command=save_text, bg="#1abc9c", fg="white", font=("Helvetica", 10))
    save_button.pack(side=tk.LEFT, padx=10)

    # Abbrechen-Button erstellen
    cancel_button = tk.Button(button_frame, text="Abbrechen", command=cancel, bg="#e74c3c", fg="white", font=("Helvetica", 10))
    cancel_button.pack(side=tk.RIGHT, padx=10)

# Funktion zum Hochladen einer Datei (Bild oder PDF) und Hinzufügen einer Beschreibung
def upload_file(file_type):
    def save_file():
        if file_type == "image":
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        else:
            file_path = filedialog.askopenfilename(
                filetypes=[("PDF files", "*.pdf")])
        
        if file_path:
            entered_text = desc_entry.get("1.0", tk.END).strip()
            entries.append({'type': file_type, 'content': file_path, 'desc': entered_text})
            save_entries()
            update_display()
        # Fenster schließen
        file_window.destroy()

    def cancel():
        # Fenster ohne Speichern schließen
        file_window.destroy()

    # Neues Fenster für das Hochladen von Dateien und Eingabe einer Beschreibung erstellen
    file_window = tk.Toplevel(root)
    file_window.title("Datei Hochladen")
    file_window.geometry("400x300")
    file_window.configure(bg="#2c3e50")

    # Textfeld für die Beschreibung erstellen
    desc_entry = tk.Text(file_window, wrap=tk.WORD, height=5, bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 12))
    desc_entry.pack(expand=True, fill=tk.BOTH, padx=10, pady=(10, 0))
    desc_entry.focus_set()

    # Rahmen für die Buttons erstellen
    button_frame = tk.Frame(file_window, bg="#2c3e50")
    button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

    # Speichern-Button erstellen
    save_button = tk.Button(button_frame, text="Datei auswählen und Speichern", command=save_file, bg="#1abc9c", fg="white", font=("Helvetica", 10))
    save_button.pack(side=tk.LEFT, padx=10)

    # Abbrechen-Button erstellen
    cancel_button = tk.Button(button_frame, text="Abbrechen", command=cancel, bg="#e74c3c", fg="white", font=("Helvetica", 10))
    cancel_button.pack(side=tk.RIGHT, padx=10)

# Funktion zum Löschen eines Eintrags
def delete_entry(index):
    # Eintrag aus der Liste entfernen
    del entries[index]
    save_entries()
    # Anzeige aktualisieren
    update_display()

# Funktion zum Herunterladen einer Datei
def download_file(file_path):
    save_path = filedialog.asksaveasfilename(initialfile=file_path.split('/')[-1])
    if save_path:
        try:
            shutil.copy(file_path, save_path)
            messagebox.showinfo("Erfolg", "Datei erfolgreich gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Datei: {str(e)}")

# Funktion zum Scrollen mit dem Mausrad
def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Funktion zum Aktualisieren der Anzeige
def update_display():
    # Vorherige Widgets im Anzeigerahmen entfernen
    for widget in display_frame.winfo_children():
        widget.destroy()

    # Jeden Eintrag mit einem Löschen-Button und einem Download-Button anzeigen
    for index, entry in enumerate(entries):
        entry_frame = tk.Frame(display_frame, relief=tk.RAISED, borderwidth=1, bg="#34495e")
        entry_frame.pack(fill=tk.X, padx=5, pady=5)

        if entry['type'] == 'text':
            # Label zum Anzeigen des Text-Eintrags
            entry_label = tk.Label(entry_frame, text=entry['content'], anchor="w", bg="#34495e", fg="white", font=("Helvetica", 12))
            entry_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        elif entry['type'] == 'image':
            # Bild laden und anzeigen
            image = Image.open(entry['content'])
            image.thumbnail((200, 200))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(entry_frame, image=photo, bg="#34495e")
            image_label.image = photo
            image_label.pack(side=tk.LEFT, padx=5, pady=5)

            # Beschreibung anzeigen
            desc_label = tk.Label(entry_frame, text=entry['desc'], anchor="w", bg="#34495e", fg="white", font=("Helvetica", 12))
            desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        elif entry['type'] == 'pdf':
            # PDF-Dateiname anzeigen
            pdf_label = tk.Label(entry_frame, text="PDF: " + entry['content'].split('/')[-1], anchor="w", bg="#34495e", fg="white", font=("Helvetica", 12))
            pdf_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

            # Beschreibung anzeigen
            desc_label = tk.Label(entry_frame, text=entry['desc'], anchor="w", bg="#34495e", fg="white", font=("Helvetica", 12))
            desc_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Löschen-Button erstellen
        delete_button = tk.Button(entry_frame, text="X", command=lambda i=index: delete_entry(i), bg="#e74c3c", fg="white", font=("Helvetica", 10))
        delete_button.pack(side=tk.RIGHT, padx=5)

        # Download-Button erstellen
        if entry['type'] in ['image', 'pdf']:
            download_button = tk.Button(entry_frame, text="Herunterladen", command=lambda path=entry['content']: download_file(path), bg="#3498db", fg="white", font=("Helvetica", 10))
            download_button.pack(side=tk.RIGHT, padx=5)

# Hauptfenster erstellen
root = tk.Tk()
root.title("ToDo by Wenger")
root.configure(bg="#2c3e50")

# Hauptfenstergröße festlegen
root.geometry("600x400")

# Liste zum Speichern der Einträge
entries = load_entries()

# Rahmen für die Buttons unten im Hauptfenster erstellen
frame = tk.Frame(root, bg="#2c3e50")
frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Drei Spalten im Raster-Layout für die Buttons erstellen
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

# Rahmen zum Anzeigen der gespeicherten Einträge mit Scrollbar
canvas = tk.Canvas(root, bg="#2c3e50")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#2c3e50")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Bind MouseWheel event to the canvas
canvas.bind_all("<MouseWheel>", on_mouse_wheel)

display_frame = tk.Frame(scrollable_frame, bg="#2c3e50")
display_frame.pack(fill="both", expand=True)

# Button "Neuer Eintrag" erstellen
button1 = tk.Button(frame, text="Neuer Eintrag", command=lambda: button_click(1), bg="#1abc9c", fg="white", font=("Helvetica", 12))
button1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Button "Bild hochladen" erstellen
button2 = tk.Button(frame, text="Bild hochladen", command=lambda: button_click(2), bg="#3498db", fg="white", font=("Helvetica", 12))
button2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Button "PDF hochladen" erstellen
button3 = tk.Button(frame, text="PDF hochladen", command=lambda: button_click(3), bg="#9b59b6", fg="white", font=("Helvetica", 12))
button3.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

# Anzeige aktualisieren
update_display()

# Hauptschleife starten
root.mainloop()
