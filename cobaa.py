import streamlit as st
import pickle
import numpy as np
import os

# Styling
st.markdown("""
    <style>
        .option-box {
            border: 2px solid #ccc;
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            cursor: pointer;
            display: flex;
            align-items: center;
        }
        .option-box:hover {
            background-color: #f1f1f1;
        }
        .selected {
            border-color: #4caf50 !important;
            background-color: #e8f5e9 !important;
        }
        .custom-image {
            margin-top: 50px;  /* Sesuaikan nilai untuk posisi gambar */
        }
        .title-section {
        text-align: left;
        }
        .content-section {
        text-align: left;
        }
    </style>
""", unsafe_allow_html=True)


# Inisialisasi scaler jika file ada
if os.path.exists('scaler.sav'):
    with open('scaler.sav', "rb") as f:
        scaler = pickle.load(f)

# Menambahkan session state untuk mengelola halaman yang dipilih
if "selected" not in st.session_state:
    st.session_state.selected = "Home"

# Navigasi Sidebar
with st.sidebar:
    selected = option_menu("NextVerse", ["Home", "Cek Kesiapan"], 
                           icons=["house", "clipboard"], 
                           menu_icon="menu-app-fill", default_index=0)
    
    # Update session state when the sidebar option is clicked
    st.session_state.selected = selected


# Data kecerdasan dan jurusan
kecerdasan = {
    1: "Kecerdasan linguistik adalah kemampuan untuk menyusun pikiran dengan jelas melalui kata-kata.",
    2: "Kecerdasan logika matematika adalah kemampuan untuk memahami angka dan pola.",
    3: "Kecerdasan spasial adalah kemampuan untuk berpikir dalam bentuk visual.",
    4: "Kecerdasan musikal adalah kemampuan untuk mengembangkan dan menikmati musik.",
    5: "Kecerdasan kinestetik adalah kemampuan menggunakan tubuh untuk beraktivitas.",
    6: "Kecerdasan interpersonal adalah kemampuan berkomunikasi dan berempati dengan orang lain.",
    7: "Kecerdasan intrapersonal adalah kemampuan untuk mengenali diri sendiri.",
    8: "Kecerdasan naturalistik adalah kemampuan untuk memahami dunia alami."
}

jurusan = {
    1: ["Ilmu Perpustakaan", "Ilmu Komunikasi", "Bahasa dan Sastra", "Ilmu Hukum"],
    2: ["Statistika", "Akuntansi", "Ilmu Ekonomi", "Teknik Informatika"],
    3: ["Seni Rupa", "Teknik Arsitektur", "Teknik Sipil"],
    4: ["Seni Musik"],
    5: ["Kedokteran Gigi", "Kebidanan", "PJKR"],
    6: ["Ilmu Sosiologi", "Psikologi", "Ilmu Keperawatan"],
    7: ["Ilmu Agama", "Administrasi Niaga"],
    8: ["Ilmu Biologi", "Teknologi Pertanian", "Ilmu Kelautan"]
}

fakta = {
        1: "Apakah anda suka membaca",
        2: "Apakah anda suka mengeksplorasi berbagai ide dan konsep dalam tulisan saya",
        3: "Apakah anda memiliki kosakata yang luas",
        4: "Apakah anda gemar menyelesaikan teka-teki silang dan mencari kata-kata",
        5: "Apakah anda gemar bercerita tentang humor, teka-teki, dan dongeng",
        6: "Apakah anda suka berpidato dan berdebat",
        7: "Acara tv favorit ku adalah acara acar komedi",
        8: "Jika mendapatkan hadiah, saya akan memilih buku",
        9: "Pelajaran favorit saya adalah Bahasa",
        10: "Saya senang belajar secara bertahap",
        11: "Saya suka menyelesaikan masalah",
        12: "Saya menikmati menjelaskan cara kerja suatu hal kepada orang lain bekerja dengan angka itu menyenangkan",
        13: "Saya suka melakukan eksperimen ilmiah",
        14: "Saya merasa puas dengan segala hal yang bersifat logis",
        15: "Acara tv favoritku adalah acara dokumenter",
        16: "Jika ada yang berniat memberi hadiah kepada saya, saya akan memilih game computer",
        17: "Pelajaran favorit saya adalah matematika dan ilmu pengetahuan alam",
        18: "Saya suka menggambar dan melukis",
        19: "Saya menikmati membuat model, mural, dan kolase",
        20: "Saya gemar memanfaatkan gambar dan diagram dalam proses belajar",
        21: "Saya mampu membayangkan hasil akhir di dalam pikiran saya",
        22: "Warna sangat penting bagi saya",
        23: "Saya mampu membayangkan peta dalam benak saya",
        24: "Saya lebih suka menonton acara televisi yang menampilkan seni dan kerajinan tangan",
        25: "Jika seseorang ingin memberikan saya hadiah, saya akan memilih puzzle",
        26: "Pelajaran favorit saya adalah seni",
        27: "Saya sengat menyukai Berkolaborasi dengan orang lain",
        28: "Saya suka menolong orang lain",
        29: "Saya suka bertemu orang orang baru",
        30: "Saya suka olahraga dalam tim",
        31: "Saya memiliki banyak teman",
        32: "Saya memiliki banyak gagasan untuk kelas kita",
        33: "Acara tv favoritku adalah drama",
        34: "Jika diberi pilihan hadiah, saya akan memilih untuk mendapatkan pengalaman liburan atau berwisata dengan teman-teman.",
        35: "Saya merasa senang saat bekerja dalam kelompok di sekolah.",
        36: "Saya menyukai potografi",
        37: "Saya suka mendaki bukit",
        38: "Saya mempunyai hewan peliharaan",
        39: "Saya senang berkebun",
        40: "Saya lebih suka menonton acara televisi yang membahas tentang alam.",
        41: "Saya senang Saya merasa senang ketika bekerja dalam kelompok di sekolah.",
        42: "Jika ada yang ingin memberi saya hadiah, saya lebih memilih untuk pergi ke kebun Binatang atau melakukan kegiatan outbound.",
        43: "Saya lebih suka berada di luar ruangan",
        44: "Saya peduli terhadap lingkungan dengan cara melakukan daur ulang.",
        45: "Saya menikmati olahraga",
        46: "Saya suka bekerja menggunakan tangan",
        47: "Saya lebih mudah memahami dan belajar ketika langsung terlibat dalam kegiatan praktis atau pengalaman langsung, daripada hanya mendengarkan atau membaca teori.",
        48: "Saya menyukai akting",
        49: "Saya suka bergerak saat bekerja",
        50: "Saya lebih menyukai program olah raga televisi",
        51: "Jika di beri hadiah saya lebih memilih alat olah raga",
        52: "Saya suka menari",
        53: "Kegiatan favorit saya disekolah adalah drama",
        54: "Saya senang mengerjakan sendiri",
        55: "Saya senang memikirkan hal-hal secara intelektual.",
        56: "Saya sering mengevaluasi diri",
        57: "Saya menulis buku atau jurnal harian.",
        58: "Saya sering mengira ngira apa yang di pikirkan orang",
        59: "Jika di beri hadiah saya lebih memilih diary atau buku harian",
        60: "Saya suka memikirkan perasaan saya",
        61: "Saat-saat menyenangkan di sekolah adalah saat diberi kebebasan untuk memilih tugas sendiri.",
        62: "Saya suka menetapkan tujuan",
        63: "Saya senang menyanyi",
        64: "Saya menikmati mendengarkan musik",
        65: "Saya merasa bahwa suara adalah hal yang menarik.",
        66: "Saya senang memainkan alat musik",
        67: "Kadang saya menciptakan lagu sendiri",
        68: "Saya sering menggerakkan kaki atau jemari mengikuti irama saat mendengarkan musik.",
        69: "Program televisi favoritsaya adalah acara music",
        70: "Jika di beri Saya lebih suka mendapatkan kaset atau CD lagu-lagu sebagai hadiah",
        71: "Mata pelajaran favorit saya adalah music",
}

# Aturan kecerdasan yang terkait dengan fakta
aturan = {
        1: [1, 2, 3, 4, 5, 6, 7, 8, 9], # Fakta terkait Linguistic-Verbal
        2: [10, 11, 12, 13, 14, 15, 16, 17], # Fakta terkait Logika-Matematik
        3: [18, 19, 20, 21, 22, 23, 24,25,26], # Fakta terkait Spasial-Visual
        4: [27, 28, 29, 30, 31, 32, 33, 34, 35], # Fakta terkait Interpersonal
        5: [36, 37, 38, 39, 40, 41, 42, 43, 44], # Fakta terkait Naturalis
        6: [45, 46, 47, 48, 49, 50, 51, 52, 53], # Fakta terkait Kinestetik
        7: [54, 55, 56, 57, 58, 59, 60, 61, 62], # Fakta terkait Intrapersonal
        8: [63, 64, 65, 66, 67, 68, 69, 70, 71], # Fakta terkait Musik-Ritmik
}

# Fungsi untuk mencocokkan fakta dengan kecerdasan
def cari_kecerdasan(input_fakta):
    hasil = []
    for id_kecerdasan, fakta_aturan in aturan.items():
        match_count = sum(1 for f in fakta_aturan if f in input_fakta)
        if match_count >= 7:  # Ambang batas kecocokan
            hasil.append(kecerdasan[id_kecerdasan])
    return hasil

# Fungsi untuk menentukan jurusan berdasarkan kecerdasan
def tentukan_jurusan(kecerdasan_terpilih):
    hasil_jurusan = []
    for id_kecerdasan, nama_kecerdasan in kecerdasan.items():
        if nama_kecerdasan in kecerdasan_terpilih:
            hasil_jurusan.extend(jurusan[id_kecerdasan])
    return hasil_jurusan

# Fungsi untuk menentukan jurusan berdasarkan kecerdasan
def tentukan_jurusan(kecerdasan_terpilih):
    hasil_jurusan = []
    for id_kecerdasan, nama_kecerdasan in kecerdasan.items():
        if nama_kecerdasan in kecerdasan_terpilih:
            hasil_jurusan.extend(jurusan[id_kecerdasan])
    return hasil_jurusan

# Halaman Home
if selected == "Home":
    # Membuat dua kolom (kolom kiri untuk teks, kolom kanan untuk gambar)
    col1, col2 = st.columns([1, 1])  # Ratio kolom kiri (lebih besar) dan kolom kanan (lebih kecil)

    # Menampilkan salam dengan format markdown dan emoji
    with col1:
        st.markdown("# Halo, Calon Mahasiswa Sukses! 🎓")
        st.markdown("### Pusing pilih jurusan?")
        
        # Pesan deskripsi dengan font yang lebih besar dan lebih rapi
        st.markdown("<p style='font-size: 16px;'>Jangan khawatir, kami punya solusi cerdas buat kamu! Sistem kami akan membantu memetakan minat dan bakatmu, lalu mencocokannya dengan jurusan yang paling tepat. Karena kuliah itu soal minat, bukan ikut-ikutan! 😊</p>", unsafe_allow_html=True)

        # Menambahkan paragraf dengan HTML untuk styling lebih lanjut
        st.markdown("<p style='font-size: 16px;'>Kalian bisa pilih menu di sebelah kiri untuk mulai menggunakan aplikasi ini.</p>", unsafe_allow_html=True)
    
        # Pemisah (line separator) antara bagian informasi
        st.markdown("---")

    with col2:
        st.markdown('<div class="custom-image">', unsafe_allow_html=True)
        st.image("https://i.pinimg.com/736x/8f/66/d2/8f66d2d2632f1abb5eff2f3e4c01fd08.jpg",  use_column_width=False, width=600)  # Gambar memenuhi kolom
        st.markdown('</div>', unsafe_allow_html=True)


# Halaman Hitung Persiapan
if selected == 'Cek Kesiapan':
    st.title('Yuk, Jawab pertanyaan berikut sesuai dengan keadaanmu saat ini')

    # Instruksi untuk pengguna
    st.markdown("""
    Di sini, Kamu akan diminta untuk menjawab beberapa pernyataan dengan memilih **'Ya'** atau **'Tidak'** untuk setiap pertanyaan.  
    """)

    # Input Fakta dari Pengguna
    input_fakta = []
    for id_fakta, pernyataan in fakta.items():
    # Tampilkan nomor dan pertanyaan
        st.write(f"**{id_fakta}. {pernyataan}**")  # Nomor dan pertanyaan yang terformat
        
        
        # Buat kotak container untuk pilihan "Ya" dan "Tidak"
        with st.container():
            # Pilihan Ya atau Tidak yang tampil dalam satu baris
            pilihan = st.radio('', ('Ya', 'Tidak'), index=None, horizontal=True, key=f"radio_{id_fakta}")

            # Menambahkan jawaban yang dipilih ke list input_fakta jika memilih 'Ya'
            if pilihan == 'Ya':
                input_fakta.append(id_fakta)

    # Proses dan tampilkan hasil
    if st.button("Cek Kesiapan"):
        kecerdasan_terpilih = cari_kecerdasan(input_fakta)
        if kecerdasan_terpilih:
            st.subheader("Jenis Kecerdasan yang Cocok dengan Kamu")
            for k in kecerdasan_terpilih:
                st.write(f"- {k}")
            
            jurusan_rekomendasi = tentukan_jurusan(kecerdasan_terpilih)
            st.subheader("Rekomendasi Jurusan Buat Kamu:")
            for j in jurusan_rekomendasi:
                st.write(f"- {j}")
        else:
            st.warning("Maaf, tidak ada kecerdasan yang cocok berdasarkan jawaban Anda.")
            
elif selected == 'Setting':
    st.title('Pengaturan Aplikasi')
    st.write("Halaman untuk mengatur konfigurasi aplikasi akan ada di sini.")
