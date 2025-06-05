import streamlit as st
from PIL import Image
import os
from datetime import datetime
import base64

st.set_page_config(layout="wide", page_title="PROGAM IP4T", initial_sidebar_state="auto")

# Function to display and center the logo in the sidebar
def display_logo():
    logo_path = 'logo.png'  # Adjust path to your logo file
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()
        st.sidebar.markdown(
            f"""
            <div style="text-align: center;">
                <img src="data:image/png;base64,{encoded_image}" width="150" />
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.sidebar.error(f"Logo file '{logo_path}' not found. Please ensure the file is in the correct directory.")

# Function to display the header

def display_header():
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <h1 style="
                color: white;
                background-color: #11009E;
                border-radius: 20px;
                padding: 20px;
                display: inline-block;
                font-size: 22px;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
            ">
                PROGRAM INVENTARISASI PENGUASAAN, PEMILIKAN, PENGGUNAAN, DAN PEMANFAATAN TANAH (IP4T)
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    

# Function to display the current date and time
def tampilkan_tanggal():
    now = datetime.now()
    tanggal = now.strftime("%A, %d-%m-%Y")
    st.markdown(f"""
        <div style='text-align: right; color: #1E3A8A; font-weight: bold; font-size: 0.9rem;'>
            <br>
                {tanggal}
            <br>
        </div>
    """, unsafe_allow_html=True)

# Function to display data information
def display_data_info():
    st.markdown("""
    <div style="color: #000; font-size: 19px; text-align: justify; line-height: 1.6;">
        <strong>IP4T</strong> (Inventarisasi Penguasaan, Pemilikan, Penggunaan, dan Pemanfaatan Tanah) adalah kegiatan pendataan yang dilakukan untuk mengidentifikasi dan mendokumentasikan informasi mengenai tanah, termasuk siapa yang menguasai, memiliki, menggunakan, dan memanfaatkan tanah tersebut. 
                <br><br>Kegiatan ini bertujuan untuk memberikan kepastian hukum dan informasi yang akurat tentang status tanah. IP4T digunakan sebagai dasar dalam pengambilan kebijakan yang berkaitan dengan <strong>optimalisasi lahan</strong>, <strong>penyelesaian konflik agraria</strong>, serta dukungannya terhadap pelaksanaan <strong>reforma agraria</strong>.
                <br><br>
                Dasar hukum pelaksanaan program IP4T merujuk pada <strong>Undang-Undang Nomor 5 Tahun 1960</strong> tentang <em>Ketentuan Pokok-Pokok Agraria (UUPA)</em>, yang menjadi landasan hukum utama dalam pengaturan agraria di Indonesia. Undang-undang ini lahir sebagai bentuk <strong>reformasi agraria</strong> untuk mengatasi ketimpangan penguasaan tanah, meningkatkan kesejahteraan rakyat, dan menciptakan keadilan agraria yang merata di seluruh wilayah Indonesia.
    </div>

    <br>

    <span style="color: #0F2167; font-size: 35px; font-weight: bold; text-decoration: underline">Pengumpulan Data</span>
    <div style="color: #000; font-size: 19px; text-align: justify; margin-top: 10px;">
        Data yang digunakan dalam penelitian ini diperoleh di <strong>Kantor Badan Pertanahan Nasional (BPN) Kabupaten Sukabumi</strong>. Permintaan data dilakukan secara resmi kepada pihak BPN untuk memperoleh informasi terkait penguasaan, pemilikan, penggunaan,pemanfaatan, dan luas tanah dari progam IP4T di wilayah tersebut. Data yang diperoleh sebanyak 1250 data.
    </div>
    <br>

    <span style="color: #0F2167; font-size: 35px; font-weight: bold; text-decoration: underline;">Data Columns</span>
    
   
    <div style="color: #000000; font-size: 16px;">
        <ol>
            Data yang diperlukan pada penelitian ini berupa data IP4T yang terdiri dari atribut Luas, penggunaan tanah, pemanfaatan tanah, pemilikan tanah, penguasaan tanah, dan potensi TOL (Tanah Objek Landreform).
            <br><br>
            <li><code>POTENSI TOL</code> dalam konteks reforma agraria adalah tanah yang memiliki peluang atau kapasitas untuk didistribusikan kembali sebagai bagian dari program reforma agraria guna mengurangi ketimpangan penguasaan dan kepemilikan tanah. Potensi TOL (Tanah Objek Landreform) terdiri 4 kelas yaitu:
                <ul>
                    <li><strong>Akses Reform</strong>: Penataan kembali struktur penguasaan, pemilikan, penggunaan, dan pemanfaatan tanah yang lebih berkeadilan melalui Penataan Aset dan Penataan Akses untuk kemakmuran rakyat.</li>
                    <li><strong>Potensi TORA</strong>: Tanah yang dikuasai oleh negara dan/atau tanah yang telah dimiliki, dikuasai, dan/atau dimanfaatkan oleh masyarakat untuk diredistribusi atau dilegalisasi.</li>
                    <li><strong>Sengketa, Konflik dan Perkara</strong>: Perselisihan agraria antara orang perorangan dan/ atau kelompok masyarakat dengan badan hukum dan/atau instansi pemerintah yang mempunyai kecenderungan atau berdampak luas secara fisik, sosial, politis, ekonomi, pertahanan atau budaya. </li>
                    <li><strong>Legalisasi aset</strong>: Proses pendaftaran tanah untuk pertama kali dan pemeliharaan data tanah yang bertujuan memberikan kepastian hukum atas kepemilikan dan penguasaan tanah kepada masyarakat, khususnya petani dan subjek reforma agraria lainnya.</li>
                </ul>
            </li>
            <li><code>Luas  m2</code>: Luas area tanah yang diamati.</li>
            <li><code>PENGGUNAAN TANAH</code>: Jenis penggunaan tanah pada area tersebut.</li>
            <li><code>PEMANFAATAN TANAH</code>: Bentuk atau cara tanah tersebut dimanfaatkan dalam praktik, yang bisa berbeda dari penggunaan.</li>
            <li><code>PEMILIKAN TANAH</code>: Informasi mengenai siapa pemilik tanah tersebut.</li>
            <li><code>PENGUASAAN TANAH</code>: Status penguasaan atas tanah tersebut.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)


# Display content for the single page
display_logo()
display_header()
tampilkan_tanggal()
display_data_info()

# Info message with a link to the dataset
st.info('Dokumentasi project ini dapat diakses melalui GitHub: [AplikasiPotensiTOLSMOTE](https://github.com/putrifahriani29/Aplikasiprediksi-smote)')
