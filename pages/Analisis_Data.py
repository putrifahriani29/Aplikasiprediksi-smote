import streamlit as st
import pandas as pd
import numpy as np
import base64
import os
import time
from datetime import datetime
from io import StringIO
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report
from imblearn.over_sampling import SMOTE

# Set layout Streamlit
st.set_page_config(layout="wide", page_title="Analisis Dataset", initial_sidebar_state="auto")

# Fungsi tampilkan waktu
def tampilkan_tanggal():
    now = datetime.now()
    tanggal = now.strftime("%A, %d-%m-%Y")
    st.markdown(f"""
        <div style='text-align: right; color: #1E3A8A; font-weight: bold; font-size: 0.9rem;'>
            {tanggal}
        </div>
    """, unsafe_allow_html=True)

def styled_header(judul_emoji_dan_teks):
    st.markdown(f"""
    <span style="color: #0F2167; font-size: 28px; font-weight: bold; ">
    {judul_emoji_dan_teks}
    </span>
    """, unsafe_allow_html=True)

# Sidebar Logo
def display_logo():
    logo_path = 'logo.png'
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
        st.sidebar.error(f"Logo file '{logo_path}' tidak ditemukan.")

# Tampilkan tanggal


tampilkan_tanggal()

# Judul halaman
st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <h1 style="
            color: white;
            background-color: #11009E;
            border-radius: 20px;
            padding: 20px;
            display: inline-block;
            font-size: 22px;
            text-transform: uppercase;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
        ">
            ANALISIS DATASET PROGRAM IP4T DAN MODEL RANDOM FOREST CLASSIFIER
        </h1>
    </div>
""", unsafe_allow_html=True)

st.info("Silakan klik tombol 'Analisis Dataset'", icon="ℹ️")

# Tombol Analisis Dataset
if st.button("📂 Analisis Dataset"):
    progress = st.progress(0, text="⏳ Memulai analisis...")
    for i in range(1, 6):
        time.sleep(0.1)
        progress.progress(i * 20, text=f"⏳ Memproses langkah {i}/5...")

    df = pd.read_csv("dataset28052025.csv", sep=";")
    st.info("Menggunakan dataset default.")
        

    if "NO" in df.columns:
        df.drop(columns=["NO"], inplace=True)

    progress.progress(100, text="Analisis selesai!")

    styled_header("Data Awal")
    st.dataframe(df.head())

    styled_header("Struktur DataFrame")
    buffer = StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    styled_header("Deskripsi Data Numerik")
    st.dataframe(df.describe().T)

    styled_header("Deskripsi Data Kategori Nominal")
    kategorik_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if kategorik_cols:
        tabs_kat = st.tabs(kategorik_cols)
        for tab, col in zip(tabs_kat, kategorik_cols):
            with tab:
                freq = df[col].value_counts()
                st.dataframe(freq, use_container_width=True)
    else:
        st.info("Tidak ada kolom kategorik ditemukan.")

    # --- Visualisasi Data Numerik (Luas Tanah) ---
    styled_header("Visualisasi Data Numerik (Luas Tanah)")

    if "Luas  m2" in df.columns:
        df["Luas  m2"] = pd.to_numeric(df["Luas  m2"], errors="coerce")
        df_luas = df.dropna(subset=["Luas  m2"])

        if not df_luas.empty:
            pastel_colors = "#FC00D2"  # Skema warna pastel
            tabs = st.tabs(["Violin Plot", "Boxplot", "Histogram"])

            with tabs[0]:
                fig_violin = px.violin(
                    df_luas, 
                    y="Luas  m2", 
                    box=True, 
                    points="all", 
                    color_discrete_sequence=[pastel_colors]
                )
                st.plotly_chart(fig_violin, use_container_width=True)

            with tabs[1]:
                fig_box = px.box(
                    df_luas, 
                    y="Luas  m2", 
                    color_discrete_sequence=[pastel_colors]
                )
                st.plotly_chart(fig_box, use_container_width=True)

            with tabs[2]:
                hist_fig = go.Figure()
                hist_fig.add_trace(go.Histogram(
                    x=df_luas["Luas  m2"],
                    nbinsx=30,
                    histnorm='density',
                    marker_color=pastel_colors  # Ambil warna pertama dari skema pastel
                ))
                st.plotly_chart(hist_fig, use_container_width=True)
        else:
            st.warning("Data Luas Tanah kosong atau tidak valid.")
    else:
        st.warning("Kolom 'Luas  m2' tidak ditemukan.")


    styled_header("Visualisasi TARGET")
    col1, col2 = st.columns(2)
    if "POTENSI TOL" in df.columns:
        potensi_tol_data = df["POTENSI TOL"].value_counts().reset_index()
        potensi_tol_data.columns = ["POTENSI TOL", "Count"]

        fig_bar = px.bar(
            potensi_tol_data,
            x="POTENSI TOL",
            y="Count",
            title="BARPLOT POTENSI TOL",
            labels={"POTENSI TOL": "Potensi TOL", "Count": "Jumlah Data"},
            color="POTENSI TOL",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bar.update_layout(showlegend=False)
        col1.plotly_chart(fig_bar, use_container_width=True)

        fig_pie = px.pie(
            potensi_tol_data,
            names="POTENSI TOL",
            values="Count",
            title="DISTRIBUSI POTENSI TOL (%)",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent')
        col2.plotly_chart(fig_pie, use_container_width=True)
    else:
        col1.info("Kolom 'POTENSI TOL' tidak ditemukan pada data.")
        col2.info("Kolom 'POTENSI TOL' tidak ditemukan pada data.")

    if "POTENSI TOL" in df.columns:
        try:
            X = df.drop(columns=["POTENSI TOL"])
            y = df["POTENSI TOL"]

           # Split data: 20% train, 80% test
            X_train_raw, X_test_raw, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            # Pisahkan kolom numerik dan kategorikal pada data latih
            numerical_cols = X_train_raw.select_dtypes(include=np.number).columns.tolist()
            categorical_cols = X_train_raw.select_dtypes(include=['object', 'category']).columns.tolist()

            # One-hot encoding: fit di data train, transform di train dan test
            ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            X_train_cat_encoded = ohe.fit_transform(X_train_raw[categorical_cols])
            X_test_cat_encoded = ohe.transform(X_test_raw[categorical_cols])

            encoded_cat_cols = ohe.get_feature_names_out(categorical_cols)
            X_train_cat_df = pd.DataFrame(X_train_cat_encoded, columns=encoded_cat_cols, index=X_train_raw.index)
            X_test_cat_df = pd.DataFrame(X_test_cat_encoded, columns=encoded_cat_cols, index=X_test_raw.index)

            # Gabungkan numerik dan kategorikal encoded
            X_train_final = pd.concat([X_train_raw[numerical_cols], X_train_cat_df], axis=1)
            X_test_final = pd.concat([X_test_raw[numerical_cols], X_test_cat_df], axis=1)

            # Terapkan SMOTE pada data latih
            smote = SMOTE(random_state=42, k_neighbors=1)
            X_train_resampled, y_train_resampled = smote.fit_resample(X_train_final, y_train)

            # Visualisasi distribusi target setelah SMOTE
            styled_header("Distribusi TARGET Setelah SMOTE")

            resampled_counts = y_train_resampled.value_counts().reset_index()
            resampled_counts.columns = ["Label", "Count"]

            col1, col2 = st.columns(2)

            with col1:
                fig_resampled_bar = px.bar(
                    resampled_counts,
                    x="Label",
                    y="Count",
                    color="Label",
                    title="Distribusi POTENSI TOL Setelah SMOTE - Barplot",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig_resampled_bar, use_container_width=True)

            with col2:
                fig_resampled_pie = px.pie(
                    resampled_counts,
                    names="Label",
                    values="Count",
                    title="Distribusi POTENSI TOL Setelah SMOTE - Pie Chart",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                    hole=0.4
                )
                fig_resampled_pie.update_traces(textposition='inside', textinfo='percent')
                st.plotly_chart(fig_resampled_pie, use_container_width=True)


            # Latih model
            model = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42)
            model.fit(X_train_resampled, y_train_resampled)

            # Prediksi pada data uji
            y_pred = model.predict(X_test_final)

            # Simpan ke session state
            st.session_state['model'] = model
            st.session_state['X_final'] = pd.concat([X_train_final, X_test_final])  # jika perlu semua data
            st.session_state['classes'] = model.classes_

            # Tampilkan hasil evaluasi
            styled_header("Confusion Matrix after SMOTE")
            tab1, tab2 = st.tabs(["Confusion Matrix", "Classification Report"])

            with tab1:
                
                cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
                fig_cm, ax = plt.subplots(figsize=(8, 6))
                sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=model.classes_, yticklabels=model.classes_)
                ax.set_xlabel("Predicted")
                ax.set_ylabel("Actual")
                st.pyplot(fig_cm)

            with tab2:
                st.markdown("### Classification Report after SMOTE")
                report = classification_report(y_test, y_pred, output_dict=True, target_names=model.classes_)
                report_df = pd.DataFrame(report).transpose()
                st.dataframe(report_df)

        except Exception as e:
            st.error(f"❌ Error saat training atau evaluasi model: {e}")
    else:
        st.warning("❌ Kolom target 'POTENSI TOL' tidak ditemukan.")

    styled_header("🌳 Visualisasi Pohon Keputusan")
    st.info("Silahkan Input di _sidebar_ !")

with st.sidebar:
    styled_header("🌲 Visualisasi Pohon")
    st.info("Silahkan Input untuk menampilkan _Decision Tree_ ke- setelah 'Analisis Dataset'")
    n_tree_sidebar = st.number_input("Pohon Ke- (1 - 100):", min_value=1, max_value=100, value=1, step=1)
    tampilkan_pohon = st.button("Tampilkan Pohon")
    display_logo()

if tampilkan_pohon:
    if 'model' in st.session_state and 'X_final' in st.session_state:
        model = st.session_state['model']
        X_final = st.session_state['X_final']

        styled_header(f"Decision Tree Ke-{n_tree_sidebar} pada Model Random Forest")
        from sklearn.tree import plot_tree
        fig_tree, ax_tree = plt.subplots(figsize=(20, 10))
        plot_tree(
            model.estimators_[n_tree_sidebar-1],
            feature_names=X_final.columns,
            class_names=model.classes_,
            filled=True,
            rounded=True,
            fontsize=8,
            ax=ax_tree
        )
        st.pyplot(fig_tree)
    else:
        st.error("Model belum dilatih. Silakan klik tombol 'Analisis Dataset' terlebih dahulu.")
