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

# Set layout
st.set_page_config(layout="wide", page_title="Analisis Dataset", initial_sidebar_state="auto")

def tampilkan_tanggal():
    now = datetime.now()
    tanggal = now.strftime("%A, %d-%m-%Y")
    st.markdown(f"""
        <div style='text-align: right; color: #1E3A8A; font-weight: bold; font-size: 0.9rem;'>
            {tanggal}
        </div>
    """, unsafe_allow_html=True)

def styled_header(judul):
    st.markdown(f"""
    <span style="color: #0F2167; font-size: 28px; font-weight: bold;">
    {judul}
    </span>
    """, unsafe_allow_html=True)

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

tampilkan_tanggal()

st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <h1 style="
            color: white;
            background-color: #11009E;
            border-radius: 20px;
            padding: 20px;
            font-size: 22px;
            text-transform: uppercase;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        ">
            ANALISIS DATASET PROGRAM IP4T DAN MODEL RANDOM FOREST CLASSIFIER
        </h1>
    </div>
""", unsafe_allow_html=True)

st.info("Klik tombol 'Analisis Dataset' untuk memulai.", icon="ℹ️")

if st.button("📂 Analisis Dataset"):
    progress = st.progress(0, text="⏳ Memulai analisis...")

    for i in range(1, 6):
        time.sleep(0.1)
        progress.progress(i * 20, text=f"⏳ Memproses langkah {i}/5...")

    df = pd.read_csv("dataset28052025.csv", sep=";")

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
                st.dataframe(df[col].value_counts())
    else:
        st.info("Tidak ada kolom kategorik ditemukan.")

    # Visualisasi Luas Tanah
    styled_header("Visualisasi Data Numerik (Luas Tanah)")
    if "Luas  m2" in df.columns:
        df["Luas  m2"] = pd.to_numeric(df["Luas  m2"], errors="coerce")
        df_luas = df.dropna(subset=["Luas  m2"])
        if not df_luas.empty:
            tabs = st.tabs(["Violin Plot", "Boxplot", "Histogram"])
            pastel_color = "#FC00D2"

            with tabs[0]:
                fig_violin = px.violin(df_luas, y="Luas  m2", box=True, points="all", color_discrete_sequence=[pastel_color])
                st.plotly_chart(fig_violin, use_container_width=True)

            with tabs[1]:
                fig_box = px.box(df_luas, y="Luas  m2", color_discrete_sequence=[pastel_color])
                st.plotly_chart(fig_box, use_container_width=True)

            with tabs[2]:
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Histogram(x=df_luas["Luas  m2"], nbinsx=30, histnorm="density", marker_color=pastel_color))
                st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.warning("Data Luas Tanah kosong atau tidak valid.")
    else:
        st.warning("Kolom 'Luas  m2' tidak ditemukan.")

    # Visualisasi Target
    styled_header("Visualisasi TARGET")
    col1, col2 = st.columns(2)
    if "POTENSI TOL" in df.columns:
        potensi_data = df["POTENSI TOL"].value_counts().reset_index()
        potensi_data.columns = ["POTENSI TOL", "Count"]

        col1.plotly_chart(px.bar(potensi_data, x="POTENSI TOL", y="Count", color="POTENSI TOL",
                                 title="BARPLOT POTENSI TOL", color_discrete_sequence=px.colors.qualitative.Pastel),
                          use_container_width=True)

        col2.plotly_chart(px.pie(potensi_data, names="POTENSI TOL", values="Count", hole=0.4,
                                 title="DISTRIBUSI POTENSI TOL (%)", color_discrete_sequence=px.colors.qualitative.Pastel)
                          .update_traces(textposition='inside', textinfo='percent'),
                          use_container_width=True)
    else:
        col1.warning("Kolom 'POTENSI TOL' tidak tersedia.")
        col2.warning("Kolom 'POTENSI TOL' tidak tersedia.")

    # Preprocessing dan Modeling
    if "POTENSI TOL" in df.columns:
        try:
            X = df.drop(columns=["POTENSI TOL"])
            y = df["POTENSI TOL"]

            X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                                        random_state=42, stratify=y)

            num_cols = X_train_raw.select_dtypes(include=np.number).columns.tolist()
            cat_cols = X_train_raw.select_dtypes(include=["object", "category"]).columns.tolist()

            ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
            X_train_cat_encoded = ohe.fit_transform(X_train_raw[cat_cols])
            X_test_cat_encoded = ohe.transform(X_test_raw[cat_cols])

            encoded_cols = ohe.get_feature_names_out(cat_cols)
            X_train_cat_df = pd.DataFrame(X_train_cat_encoded, columns=encoded_cols, index=X_train_raw.index)
            X_test_cat_df = pd.DataFrame(X_test_cat_encoded, columns=encoded_cols, index=X_test_raw.index)

            X_train_final = pd.concat([X_train_raw[num_cols], X_train_cat_df], axis=1)
            X_test_final = pd.concat([X_test_raw[num_cols], X_test_cat_df], axis=1)

            smote = SMOTE(random_state=42, k_neighbors=1)
            X_train_resampled, y_train_resampled = smote.fit_resample(X_train_final, y_train)

            styled_header("Distribusi TARGET Setelah SMOTE")
            col1, col2 = st.columns(2)
            resampled_df = y_train_resampled.value_counts().reset_index()
            resampled_df.columns = ["Label", "Count"]

            col1.plotly_chart(px.bar(resampled_df, x="Label", y="Count", color="Label",
                                     title="Distribusi POTENSI TOL Setelah SMOTE - Barplot",
                                     color_discrete_sequence=px.colors.qualitative.Set2),
                              use_container_width=True)

            col2.plotly_chart(px.pie(resampled_df, names="Label", values="Count", hole=0.4,
                                     title="Distribusi POTENSI TOL Setelah SMOTE - Pie Chart",
                                     color_discrete_sequence=px.colors.qualitative.Set2)
                              .update_traces(textposition='inside', textinfo='percent'),
                              use_container_width=True)

            model = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42)
            model.fit(X_train_resampled, y_train_resampled)

            y_pred = model.predict(X_test_final)

            st.session_state['model'] = model
            st.session_state['X_final'] = pd.concat([X_train_final, X_test_final])
            st.session_state['classes'] = model.classes_

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
                st.markdown("### Classification Report")
                report = classification_report(y_test, y_pred, output_dict=True, target_names=model.classes_)
                st.dataframe(pd.DataFrame(report).transpose())
        except Exception as e:
            st.error(f"Terjadi kesalahan saat training model: {e}")
    else:
        st.warning("Kolom 'POTENSI TOL' tidak tersedia.")

    styled_header("🌳 Visualisasi Pohon Keputusan")
    st.info("Silahkan input pohon yang ingin divisualisasikan di sidebar.")

# Sidebar
with st.sidebar:
    styled_header("🌲 Visualisasi Pohon")
    n_tree_sidebar = st.number_input("Pohon Ke- (1 - 100):", min_value=1, max_value=100, value=1, step=1)
    tampilkan_pohon = st.button("Tampilkan Pohon")
    display_logo()

if tampilkan_pohon:
    if 'model' in st.session_state and 'X_final' in st.session_state:
        from sklearn.tree import plot_tree
        model = st.session_state['model']
        X_final = st.session_state['X_final']

        styled_header(f"Decision Tree Ke-{n_tree_sidebar}")
        fig_tree, ax_tree = plt.subplots(figsize=(20, 10))
        plot_tree(model.estimators_[n_tree_sidebar - 1],
                  feature_names=X_final.columns,
                  class_names=model.classes_,
                  filled=True, rounded=True, fontsize=8, ax=ax_tree)
        st.pyplot(fig_tree)
    else:
        st.warning("Model belum tersedia. Jalankan 'Analisis Dataset' terlebih dahulu.")
