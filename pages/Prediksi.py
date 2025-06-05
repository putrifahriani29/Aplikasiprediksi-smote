import streamlit as st
import pickle
import pandas as pd
import time
import os
import base64

# --------------------- Konfigurasi Halaman ---------------------
st.set_page_config(layout="wide", page_title="Prediksi Potensi TOL", initial_sidebar_state="auto")

# --------------------- Tampilkan Logo ---------------------
def display_logo():
    logo_path = 'logo.png'
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        st.sidebar.markdown(f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_image}" width="150" />
            </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.error(f"Logo file '{logo_path}' tidak ditemukan.")

display_logo()

# --------------------- Judul Aplikasi ---------------------
st.markdown("""
    <div style='text-align: center; color: #004AAD; background-color: #E3F2FD; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);'>
        <div style="font-size: 2.2rem; font-weight: bold;">PREDIKSI POTENSI TOL</div>
        <div style="font-size: 1.3rem; font-weight: bold;">(Tanah Objek Landreform)</div>
    </div>
""", unsafe_allow_html=True)

# --------------------- Styling Tombol ---------------------
st.markdown("""
    <style>
    /* Atur tampilan normal tombol */
    div.stButton > button {
        background-color: #007BFF;
        color: white !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 0.75em 1.5em;
        transition: background-color 0.3s ease, color 0.3s ease;
        font-size: 18px;
        width: 100%;
    }

    /* Saat hover */
    div.stButton > button:hover {
        background-color: #FFD600 !important;
        color: black !important;
    }

    /* Saat diklik (active) */
    div.stButton > button:active, div.stButton > button:focus:active {
        background-color: #FFC107 !important;
        color: black !important;
    }

    /* Saat tombol tetap fokus setelah klik */
    div.stButton > button:focus {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------- Fungsi Styling Output ---------------------
def generate_style(param_name, value, bg_color="#FFF5C2", text_color="blue"):
    return f'''
    <div style="background-color: {bg_color}; padding: 10px; border-radius: 10px; margin: 10px 0; text-align: center; font-weight: bold; color: {text_color}; box-shadow: 2px 2px 10px rgba(0,0,0,0.2); font-size: 110%;">
        {param_name}<br>
        <span style="font-size: 150%; color: #6DB9EF;">{value}</span>
    </div>
    '''

# --------------------- Load Model ---------------------
@st.cache_resource
def load_model():
    with open("model_potensiTOL+SMOTE.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# --------------------- Form Input ---------------------

penguasaan = st.selectbox("**PENGUASAAN TANAH**", ["Penggarap", "Pemilik", "Fasos Fasum", "Aset Desa", "Pemerintah"])
kepemilikan = st.selectbox("**KEPEMILIKAN TANAH**", ["Terdaftar (dari areal penyisihan HGU Lama)", "Belum Terdaftar", "Terdaftar dalam HGU baru (diluar penyisihan)", "Terdaftar (di luar areal penyisihan / tumpang tindih dengan HGU baru)","Terdaftar","Tidak terdaftar (dalam areal penyisihan HGU Lama)"])
penggunaan = st.selectbox("**PENGGUNAAN TANAH**", ["Tegalan", "Rumah Tinggal", "Kebun Campuran", "Mushola", "Masjid", "PAUD", "Posyandu","Madrasah", "Pangkalan Ojek", "Kebun","Madrasah Ibtidayah","Lapang Poli", "Bangunan Rekreasi","Fasos/Fasum/lainnya","Lapang Bola"])
pemanfaatan = st.selectbox("**PEMANFAATAN TANAH**", ["Tanaman semusim", "Tempat tinggal", "Pemanfaatan Produksi Pertanian", "Sarana Ibadah", "Sarana Pendidikan", "Olahraga", "Tempat Usaha", "Sarana Kesehatan","Pemanfaatan fasos/fasum","Tanaman Tahunan"])
luas = st.number_input("**LUAS TANAH (m²)** _maximum 50 ha_", min_value=1, max_value=500000, value=1000, step=1)

# --------------------- Tombol Prediksi ---------------------
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    submit = st.button("**TAMPILKAN PREDIKSI**")


# --------------------- Proses Prediksi ---------------------
if submit:
    
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i + 1)
    progress.empty()

    input_df = pd.DataFrame([{
        "PENGUASAAN TANAH": penguasaan,
        "PEMILIKAN TANAH": kepemilikan,
        "PENGGUNAAN TANAH": penggunaan,
        "PEMANFAATAN TANAH": pemanfaatan,
        "Luas  m2": luas
    }])

    try:
        prediksi = model.predict(input_df)[0]
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat prediksi: {e}")
        st.stop()
    
    # --------------------- Tampilkan Input ---------------------
    st.markdown("## Hasil Input Parameter")
    col1, col2 = st.columns(2)
    col1.markdown(generate_style("PENGUASAAN TANAH", penguasaan), unsafe_allow_html=True)
    col2.markdown(generate_style("KEPEMILIKAN TANAH", kepemilikan), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(generate_style("PENGGUNAAN TANAH", penggunaan), unsafe_allow_html=True)
    col2.markdown(generate_style("PEMANFAATAN TANAH", pemanfaatan), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.markdown(generate_style("LUAS TANAH (m²)", luas), unsafe_allow_html=True)
    col2.empty()

    # --------------------- Tampilkan Hasil Prediksi ---------------------
    st.markdown("## Hasil Prediksi")
    st.markdown(f"""
    <div style="margin-top: 30px; padding: 15px; background-color: #C2D5FF; border-radius: 20px; border: 4px double blue; text-align: center; font-size: 2rem; font-weight: bold; color: #B80000; box-shadow: 0 0 15px #C2D5FF;">
        <span style="text-transform: uppercase;">{prediksi}</span>
    </div>
    """, unsafe_allow_html=True)

    # --------------------- Penjelasan Hasil ---------------------
    deskripsi = {
        "Akses Reform": "Penataan kembali struktur penguasaan, pemilikan, penggunaan, dan pemanfaatan tanah yang lebih berkeadilan melalui Penataan Aset dan Penataan Akses untuk kemakmuran rakyat.",
        "Potensi TORA": "Tanah yang dikuasai oleh negara dan/atau tanah yang telah dimiliki, dikuasai, dan/atau dimanfaatkan oleh masyarakat untuk diredistribusi atau dilegalisasi.",
        "Sengketa, Konflik dan Perkara": "Perselisihan agraria antara orang perorangan dan/atau kelompok masyarakat dengan badan hukum dan/atau instansi pemerintah yang mempunyai kecenderungan atau berdampak luas secara fisik, sosial, politis, ekonomi, pertahanan atau budaya.",
        "Legalisasi aset": "Proses pendaftaran tanah untuk pertama kali dan pemeliharaan data tanah yang bertujuan memberikan kepastian hukum atas kepemilikan dan penguasaan tanah kepada masyarakat, khususnya petani dan subjek reforma agraria lainnya."
    }
    penjelasan = deskripsi.get(prediksi, "Tidak ada deskripsi tersedia untuk hasil ini.")

    st.markdown(f"""
    <div style="margin-top: 20px; padding: 15px; background-color: #F9FAFB; border-left: 6px solid #007BFF; border-radius: 10px; font-size: 1.1rem; color: #333; box-shadow: 2px 2px 12px rgba(0,0,0,0.1);">
        <strong>Penjelasan Hasil Prediksi:</strong><br>
        {penjelasan}
    </div>
    """, unsafe_allow_html=True)

  
