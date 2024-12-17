import streamlit as st
import os
import pickle
import re

# ------------------ Konfigurasi Halaman Utama ------------------
st.set_page_config(page_title="Sistem Pakar Dashboard", page_icon="🧠", layout="centered")


# ------------------ Inisialisasi Session State ------------------
if "user_authenticated" not in st.session_state:
    st.session_state["user_authenticated"] = False

if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Dashboard"

# Path ke database pengguna
user_db_path = "users.pkl"

# Fungsi untuk memuat database pengguna
def load_users():
    if os.path.exists(user_db_path):
        with open(user_db_path, "rb") as f:
            return pickle.load(f)
    return {}

# Fungsi untuk menyimpan database pengguna
def save_users(users):
    with open(user_db_path, "wb") as f:
        pickle.dump(users, f)

# Load database pengguna
users = load_users()

# Fungsi untuk memeriksa kredensial
def authenticate(username, password):
    if username in users:
        return users[username]["password"] == password
    return False

# Fungsi untuk menambah pengguna baru
def add_user(username, password, nama, email):
    if username in users:
        return False  # Username sudah ada
    users[username] = {"password": password, "nama": nama, "email": email}
    save_users(users)
    return True

# Fungsi validasi email
def validate_email(email):
    if not email.endswith("@gmail.com"):
        return "Email harus berakhiran @gmail.com."
    return None

# Fungsi validasi password
def validate_password(password):
    if len(password) < 8:
        return "Password harus memiliki minimal 8 karakter."
    if not re.search(r'[0-9]', password) and not re.search(r'[A-Za-z]', password):
        return "Password harus mengandung angka atau huruf."
    return None

# Fungsi untuk logout
def logout():
    st.session_state["user_authenticated"] = False
    st.session_state["selected_page"] = "Dashboard"
    st.rerun()

# ------------------ Halaman Dashboard ------------------
if st.session_state["selected_page"] == "Dashboard":
    col1, col2 = st.columns([1, 1])  # Ratio kolom kiri (lebih besar) dan kolom kanan (lebih kecil)

    with col1:
        st.title("Halo, Calon Mahasiswa Sukses! 🎓")

        st.write("""
            🎓 **Selamat Datang di NextVerse!** 🎓  
            Temukan jurusan kuliah yang tepat berdasarkan minat dan bakatmu. Mulai perjalananmu sekarang, kami siap membantu! 😊        
                 """)
    
    with col2:
        # Centering the image within the column
        st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%;">', unsafe_allow_html=True)
        st.image("https://i.pinimg.com/736x/6e/7d/52/6e7d5256a6293580e48fa1bf33328c45.jpg", width=400)
        st.markdown('</div>', unsafe_allow_html=True)  

    # Tombol Diagnosis
    if st.button("📝 Dapatkan Rekomendasi Jurusan"):
        if st.session_state["user_authenticated"]:
            st.success("Mengakses halaman diagnosis...")
            st.session_state["selected_page"] = "Diagnosis"
            st.rerun()
        else:
            st.warning("Silakan login terlebih dahulu untuk memulai diagnosis.")
            st.session_state["selected_page"] = "Login"
            st.rerun()

# ------------------ Halaman Login ------------------
elif st.session_state["selected_page"] == "Login":
    st.title("Selamat Datang di NextVerse 🎓")
    st.write("""
    Sebelum kita mulai mencari jurusan kuliah yang pas buat kamu, yuk login dulu!
    """)
    st.markdown("<div class='custom-login-box'>", unsafe_allow_html=True)
    
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state["user_authenticated"] = True
            st.session_state["selected_page"] = "Diagnosis"  # Langsung ke Diagnosis
            st.success("Login berhasil! Mengarahkan ke halaman diagnosis...")
            st.rerun()
        else:
            st.error("Username atau password salah.")

    # Tombol untuk berpindah ke halaman Signup
    if st.button("Belum punya akun? Daftar di sini"):
        st.session_state["selected_page"] = "Signup"
        st.rerun()

# ------------------ Halaman Register (Signup) ------------------
elif st.session_state["selected_page"] == "Signup":
    st.title("Daftar Akun Baru 📝")
    st.write("""
    Hai! Selamat datang di sistem pakar kami. Sebelum kita mulai mencari jurusan kuliah yang tepat untukmu, yuk daftar dulu!
    """)
    
    nama = st.text_input("Nama Lengkap", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    new_username = st.text_input("Username", key="signup_username")
    new_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Daftar"):
        if nama and email and new_username and new_password:
            password_error = validate_password(new_password)
            if password_error:
                st.error(password_error)
            else:
                email_error = validate_email(email)
                if email_error:
                    st.error(email_error)
                else:
                    if add_user(new_username, new_password, nama, email):
                        st.success("Akun berhasil dibuat. Silakan login.")
                        st.session_state["selected_page"] = "Login"
                        st.rerun()
                    else:
                        st.error("Username sudah digunakan. Coba username lain.")
        else:
            st.error("Mohon isi semua field.")

# ------------------ Halaman Diagnosis ------------------
elif st.session_state["selected_page"] == "Diagnosis":
    # Fungsi forward_chaining di sini
    def forward_chaining():
        st.title("🎓 Selamat Datang di Rekomendasi Jurusan NextVerse! 🎓")
        
        # Menampilkan pesan tambahan dengan emoji
            # Tampilkan teks pengantar hanya jika hasil rekomendasi belum muncul
        if st.session_state.get('hasil') is None:
            st.write("""Di halaman ini, kami akan membantu kamu menganalisis minat dan bakatmu melalui serangkaian pertanyaan. Jawablah dengan jujur, karena hasil dari diagnosis ini akan memberikan rekomendasi jurusan yang sesuai dengan dirimu.
                     """)
        else:
            st.write("Jenis kecerdasan dan rekomendasi jurusan berdasarkan minat bakat kamu:\n")

        # Inisialisasi session state
        if 'step' not in st.session_state:
            st.session_state['step'] = 1
        if 'jawaban' not in st.session_state:
            st.session_state['jawaban'] = {}
        if 'fakta' not in st.session_state:
            st.session_state['fakta'] = []
        if 'hasil' not in st.session_state:
            st.session_state['hasil'] = None  # Hasil awal belum ada

        # Daftar fakta per kecerdasan
        fakta_kecerdasan = {
            1: ["Saya suka membaca", "Saya suka mengeksplorasi berbagai ide dan konsep dalam tulisan saya", "Saya suka berpidato dan berdebat"],
            2: ["Saya senang belajar secara bertahap", "Saya suka menyelesaikan masalah", "Pelajaran favorit saya adalah matematika dan ilmu pengetahuan alam"],
            3: ["Saya suka menggambar dan melukis", "Saya lebih suka menonton acara televisi yang menampilkan seni dan kerajinan tangan", "Pelajaran favorit saya adalah seni"],
            4: ["Saya suka bertemu orang orang baru", "Saya memiliki banyak teman", "Saya merasa senang saat bekerja dalam kelompok di sekolah"],
            5: ["Saya mempunyai hewan peliharaan", "Saya senang berkebun", "Saya lebih suka berada di luar ruangan"],
            6: ["Saya menikmati olahraga", "Saya suka bekerja menggunakan tangan", "Saya suka bergerak saat bekerja"],
            7: ["Saya menulis buku atau jurnal harian", "Saya sering mengira-ngira apa yang dipikirkan orang", "Saya suka memikirkan perasaan saya"],
            8: ["Saya senang menyanyi", "Saya menikmati mendengarkan musik", "Saya senang memainkan alat musik", "Kadang saya menciptakan lagu"]
        }

        # Mapping hasil kecerdasan ke rekomendasi jurusan
        rekomendasi_jurusan = {
            1: ["Ilmu Perpustakaan", "Ilmu Komunikasi", "Bahasa dan Sastra", "Ilmu Hubungan Internasional", "Ilmu Hukum", "Ilmu Politik"],
            2: ["Statistika", "Administrasi Negara", "Akuntansi", "Ilmu Ekonomi", "Pendidikan Matematika", "Ilmu Fisika", "Teknik Informatika", "Sistem Informasi"],
            3: ["Seni Rupa", "Teknik Arsitektur", "Planologi", "Teknik Sipil"],
            4: ["Ilmu Sosiologi", "PGPAUD", "PGSD", "Psikologi", "Kedokteran", "Ilmu Keperawatan"],
            5: ["Kedokteran Hewan", "Budidaya Perikanan", "Ilmu Kelautan", "Teknologi Pertanian"],
            6: ["Kedokteran Gigi", "Seni Tari", "PJKR", "Teknik Mesin"],
            7: ["Ilmu Agama", "Administrasi Niaga"],
            8: ["Seni Musik"]
        }

        # Add descriptions for each intelligence type
        deskripsi_kecerdasan = {
            1: ("Linguistik-Verbal", 
                "Kecerdasan linguistik adalah suatu kemampuan untuk menyusun pikiran dengan jelas dan mampu menggunakan secara kompeten melalui kata kata seperti membaca, berbicara dan menulis.", 
                ["Ilmu Perpustakaan", "Ilmu Komunikasi", "Bahasa dan Sastra", "Ilmu Hubungan Internasional", "Ilmu Hukum", "Ilmu Politik"]),
            
            2: ("Logika-Matematik", 
                "Kecerdasan logika-matematik berkaitan dengan kemampuan dalam berpikir logis dan rasional, serta menyelesaikan masalah yang kompleks dan berbasis angka.", 
                ["Statistika", "Administrasi Negara", "Akuntansi", "Ilmu Ekonomi", "Pendidikan Matematika", "Ilmu Fisika", "Teknik Informatika", "Sistem Informasi"]),
            
            3: ("Spasial-Visual", 
                "Kecerdasan spasial-visual adalah kemampuan untuk memahami gambar dan ruang, serta merencanakan dan menciptakan objek dalam ruang tersebut.", 
                ["Seni Rupa", "Teknik Arsitektur", "Planologi", "Teknik Sipil"]),
            
            4: ("Interpersonal", 
                "Kecerdasan interpersonal adalah kemampuan untuk memahami orang lain, merasakan emosi mereka, dan membangun hubungan sosial yang baik.", 
                ["Ilmu Sosiologi", "PGPAUD", "PGSD", "Psikologi", "Kedokteran", "Ilmu Keperawatan"]),
            
            5: ("Naturalis", 
                "Kecerdasan naturalis melibatkan kemampuan untuk mengenali dan memahami dunia alam, termasuk flora, fauna, dan fenomena alam.", 
                ["Kedokteran Hewan", "Budidaya Perikanan", "Ilmu Kelautan", "Teknologi Pertanian"]),
            
            6: ("Kinestetik", 
                "Kecerdasan kinestetik adalah kemampuan untuk mengendalikan tubuh dan melaksanakan tugas fisik dengan baik.", 
                ["Kedokteran Gigi", "Seni Tari", "PJKR", "Teknik Mesin"]),
            
            7: ("Intrapersonal", 
                "Kecerdasan intrapersonal adalah kemampuan untuk mengenali diri sendiri dan memahami perasaan serta motivasi pribadi.", 
                ["Ilmu Agama", "Administrasi Niaga"]),
            
            8: ("Musik-Ritmik", 
                "Kecerdasan musik-ritmik berhubungan dengan kemampuan dalam mengenali dan menciptakan nada, ritme, dan suara.", 
                ["Seni Musik"])
        }
            
        # Fungsi untuk menampilkan pertanyaan dalam kotak dengan frame
        def tampilkan_pertanyaan_dalam_kotak(pertanyaan):
            st.markdown(
                f"""
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px; background-color: #f9f9f9; font-size: 16px;">
                    {pertanyaan}
                </div>
                """, unsafe_allow_html=True
            )

        # Menampilkan pertanyaan bertahap berdasarkan fakta
        step = st.session_state['step']

        # Pastikan step tidak melebihi total kecerdasan yang ada
        if step > len(fakta_kecerdasan):
            step = 1  # Mulai lagi dari awal jika step lebih dari jumlah kecerdasan

        total_fakta = len(fakta_kecerdasan[step])

        # Menampilkan pertanyaan dan tombol Lanjut
        if step in fakta_kecerdasan and st.session_state['hasil'] is None:
            current_fakta = fakta_kecerdasan[step]
            next_fakta_index = len(st.session_state['fakta'])

            if next_fakta_index < total_fakta:
                # Menampilkan pertanyaan dalam kotak
                tampilkan_pertanyaan_dalam_kotak(f"Minat bakat kamu: {current_fakta[next_fakta_index]}")

                # Menampilkan radio button untuk jawaban
                jawaban = st.radio("", ["Ya", "Tidak"], key=f"step{step}_fakta{next_fakta_index}", index=None)

                # Tombol lanjut
                lanjut_button = st.button("Lanjut")

                if lanjut_button and jawaban is not None:  # Cek jika tombol lanjut ditekan dan pilihan sudah ada
                    st.session_state['fakta'].append(jawaban)
                    if jawaban == "Tidak":
                        st.session_state['step'] += 1  # Pindah ke step berikutnya jika jawabannya "Tidak"
                        st.session_state['fakta'] = []  # Reset fakta untuk step ini
                        st.rerun()
                    else:
                        st.rerun()
            else:
                # Evaluasi jawaban fakta per kecerdasan
                if all(j == "Ya" for j in st.session_state['fakta']):
                    st.session_state['hasil'] = rekomendasi_jurusan[step]
                st.session_state['step'] += 1  # Pindah ke kecerdasan berikutnya
                st.session_state['fakta'] = []  # Reset fakta
                st.rerun()

        # ------------------ Menampilkan Hasil Diagnosis ------------------
        if 'hasil' in st.session_state and st.session_state['hasil'] is not None:
            kecerdasan_id = st.session_state['step'] - 1  # Get the corresponding intelligence ID (step-1)
            
            if kecerdasan_id in deskripsi_kecerdasan:
                # Get the description and recommended majors for the selected intelligence
                jenis_kecerdasan, deskripsi, jurusan = deskripsi_kecerdasan[kecerdasan_id]
                
                # Display the results
                st.success(f"Jenis Kecerdasan: {jenis_kecerdasan}")
                st.write(f"Deskripsi: {deskripsi}")
                st.markdown("**Jurusan Rekomendasi:**")
                for item in jurusan:
                    st.write(f"- {item}")

            # Peringatan jika tidak ada kecerdasan yang cocok
            if not kecerdasan_ditemukan:
                st.warning("Maaf, tidak ada kecerdasan yang cocok berdasarkan jawaban Anda.")
                   
                # Tombol Muat Ulang baru muncul setelah hasil
                if st.button("Dapatkan Rekomendasi Lagi"):
                    st.session_state.clear()  # Clear session state to reset everything
                    st.session_state["selected_page"] = "Diagnosis"  # Go back to the diagnosis page
                    st.rerun()  # Refresh the page to show the Diagnosis page

                # Tombol Logout di Dashboard atau Diagnosis
                if st.session_state["user_authenticated"]:
                    if st.button("Logout"):
                        logout()  # Memanggil fungsi logout untuk mengatur session dan mereload halaman
                        st.success("Berhasil logout!")
            
    # Call forward_chaining function here directly, no need for `if __name__ == "__main__":`
    forward_chaining()
