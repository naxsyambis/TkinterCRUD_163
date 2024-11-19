import sqlite3 # Mengimpor modul sqlite3 untuk bekerja dengan database SQLite.
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Mengimpor komponen GUI dari tkinter.

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat objek cursor untuk berinteraksi dengan database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (  
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama_siswa TEXT,  
            biologi INTEGER, 
            fisika INTEGER,  
            inggris INTEGER,  
            prediksi_fakultas TEXT  
        )
    ''')
    conn.commit()  # Menyimpan perubahan ke database
    conn.close()  # Menutup koneksi database

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall()  # Menyimpan hasil query ke dalam variabel rows
    conn.close()  # Menutup koneksi database
    return rows  # Mengembalikan data yang diambil

# Fungsi untuk menyimpan data ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menyisipkan data siswa ke dalam tabel
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk memperbarui data dalam database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?  # Mengupdate data berdasarkan id
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Menyisipkan data yang diperbarui
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan id
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:  # Jika nilai biologi lebih tinggi
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:  # Jika nilai fisika lebih tinggi
        return "Teknik"
    elif inggris > biologi and inggris > fisika:  # Jika nilai inggris lebih tinggi
        return "Bahasa"
    else:
        return "Tidak Diketahui"  # Jika nilai sama atau tidak lebih tinggi

# Fungsi untuk menyimpan data yang dimasukkan oleh pengguna
def submit():
    try:
        nama = nama_var.get()  # Mengambil nilai dari input nama
        biologi = int(biologi_var.get())  # Mengambil nilai dari input biologi dan mengubahnya ke integer
        fisika = int(fisika_var.get())  # Mengambil nilai dari input fisika dan mengubahnya ke integer
        inggris = int(inggris_var.get())  # Mengambil nilai dari input inggris dan mengubahnya ke integer

        if not nama:  # Mengecek apakah nama kosong
            raise Exception("Nama siswa tidak boleh kosong.")  # Memberikan pesan error jika kosong

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input form
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")  # Menampilkan pesan error jika input tidak valid

# Fungsi untuk memperbarui data yang dipilih
def update():
    try:
        if not selected_record_id.get():  # Mengecek apakah ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")  # Memberikan pesan error jika tidak ada yang dipilih

        record_id = int(selected_record_id.get())  # Mengambil id record yang dipilih
        nama = nama_var.get()  # Mengambil nama yang dimasukkan
        biologi = int(biologi_var.get())  # Mengambil nilai biologi
        fisika = int(fisika_var.get())  # Mengambil nilai fisika
        inggris = int(inggris_var.get())  # Mengambil nilai inggris

        if not nama:  # Mengecek apakah nama kosong
            raise ValueError("Nama siswa tidak boleh kosong.")  # Memberikan pesan error jika kosong

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input form
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error jika ada kesalahan

# Fungsi untuk menghapus data yang dipilih
def delete():
    try:
        if not selected_record_id.get():  # Mengecek apakah ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")  # Memberikan pesan error jika tidak ada yang dipilih

        record_id = int(selected_record_id.get())  # Mengambil id record yang dipilih
        delete_database(record_id)  # Menghapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Menampilkan pesan sukses
        clear_inputs()  # Membersihkan input form
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menampilkan pesan error jika ada kesalahan

# Fungsi untuk membersihkan input form
def clear_inputs():
    nama_var.set("")  # Mengosongkan input nama
    biologi_var.set("")  # Mengosongkan input biologi
    fisika_var.set("")  # Mengosongkan input fisika
    inggris_var.set("")  # Mengosongkan input inggris
    selected_record_id.set("")  # Mengosongkan id record yang dipilih

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():  # Menghapus semua baris di tabel
        tree.delete(row)  # Menghapus setiap baris
    for row in fetch_data():  # Menambahkan data yang diambil dari database ke tabel
        tree.insert('', 'end', values=row)  # Menambahkan data ke tabel

# Fungsi untuk mengisi input berdasarkan data yang dipilih di tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mengambil item yang dipilih dari tabel
        selected_row = tree.item(selected_item)['values']  # Mengambil data dari baris yang dipilih

        selected_record_id.set(selected_row[0])  # Mengisi id record yang dipilih
        nama_var.set(selected_row[1])  # Mengisi input nama
        biologi_var.set(selected_row[2])  # Mengisi input biologi
        fisika_var.set(selected_row[3])  # Mengisi input fisika
        inggris_var.set(selected_row[4])  # Mengisi input inggris
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")  # Menampilkan pesan error jika tidak ada data yang valid

# Inisialisasi database
create_database()  # Membuat database dan tabel jika belum ada

# Membuat GUI dengan tkinter
root = Tk()  # Membuat objek Tkinter untuk window
root.title("Prediksi Fakultas Siswa")  # Memberikan judul pada window
root.configure(bg="light blue")  # Mengatur warna background menjadi biru muda

# Variabel tkinter
nama_var = StringVar()  # Variabel untuk input nama siswa
biologi_var = StringVar()  # Variabel untuk input nilai biologi
fisika_var = StringVar()  # Variabel untuk input nilai fisika
inggris_var = StringVar()  # Variabel untuk input nilai inggris
selected_record_id = StringVar()  # Variabel untuk menyimpan ID record yang dipilih

# Membuat label dan input untuk form nama, Biologi, Fisika, dan Bahasa Inggris
Label(root, text="Nama Siswa", bg="light blue").grid(row=0, column=0, padx=10, pady=5) # Label untuk Nama
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Input untuk Nama

Label(root, text="Nilai Biologi", bg="light blue").grid(row=1, column=0, padx=10, pady=5) # Label untuk Biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5) # Input untuk Biologi

Label(root, text="Nilai Fisika", bg="light blue").grid(row=2, column=0, padx=10, pady=5) # Label untuk Fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5) # Input untuk Fisika

Label(root, text="Nilai Inggris", bg="light blue").grid(row=3, column=0, padx=10, pady=5) # Label untuk Bahasa Inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5) # Input untuk Bahasa Inggris

# Membuat tombol untuk submit, update, dan delete
Button(root, text="Add", command=submit, bg="#a8d5a2", fg="black").grid(row=4, column=0, pady=10)  # Button untuk menyimpan data berwarna hijau lembut
Button(root, text="Update", command=update, bg="#f7dc81", fg="black").grid(row=4, column=1, pady=10)  # Button untuk mengupdate data berwarna kuning lembut
Button(root, text="Delete", command=delete, bg="#f5a8a8", fg="black").grid(row=4, column=2, pady=10)  # Button untuk menghapus data berwarna merah lembut

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')  # Membuat tabel dengan kolom yang ditentukan

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())  # Menyusun judul kolom
    tree.column(col, anchor='center')  # Mengatur teks kolom agar rata tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)  # Menempatkan tabel pada grid

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Menghubungkan event klik pada tabel untuk mengisi input form

populate_table()  # Memasukkan data awal ke dalam tabel

root.mainloop()  # Menjalankan aplikasi Tkinter