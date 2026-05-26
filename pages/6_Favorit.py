import streamlit as st

from utils.helper import load_data
from utils.style import load_css
from utils.rating import get_top_rated_recipes

# Load styling halaman
load_css()

st.title("Koleksi Resep Favorit")

# =========================
# LOAD DATA
# =========================
df = load_data()

# =========================
# SESSION FAVORIT
# =========================
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

favorites = st.session_state["favorites"]

# =========================
# TAMPILAN ATAS: RESEP PILIHAN (POPULER)
# =========================
top_rated = get_top_rated_recipes()

if not top_rated.empty:
    st.markdown(
        """
        <div style="background-color:#ede0d4; padding:18px; border-radius:14px; margin-bottom:20px; border:1px solid #dbc4aa;">
            <h3 style="color:#6b4226; margin:0 0 6px 0; font-size:20px;">Resep Pilihan Pengguna</h3>
            <div style="color:#4b3a2f; font-size:14px;">Berdasarkan rating dan ulasan komunitas saat ini</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tampilkan top 5 resep populer dalam kolom horizontal agar hemat tempat
    top5 = top_rated.head(5)
    cols_top = st.columns(len(top5))
    
    for idx, (_, row) in enumerate(top5.iterrows()):
        with cols_top[idx]:
            st.markdown(
                f"""
                <div style="background-color:#fffaf3; padding:12px; border-radius:10px; border:1px solid #dbc4aa; text-align:center; min-height:90px;">
                    <b style="color:#6b4226; font-size:14px; display:block; margin-bottom:6px;">{row['recipe']}</b>
                    <span style="font-size:13px; color:#4b3a2f;">⭐ {round(row['rating'], 1)}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    st.markdown("<br>", unsafe_allow_html=True)

# =========================
# TAMPILKAN DAFTAR FAVORIT USER
# =========================
if len(favorites) == 0:
    st.markdown(
        """
        <div style="background-color:#e5e7eb; padding:40px; border-radius:18px; text-align:center; margin-top:10px; border:1px solid #cbd5e1;">
            <h2 style="color:#374151; margin-bottom:10px; font-size:22px;">Belum Ada Resep Favorit</h2>
            <p style="color:#6b7280; font-size:15px; margin:0;">
                Kamu belum menandai resep apa pun. Tambahkan resep kesukaanmu dari halaman rekomendasi ya!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div style="background-color:#ede0d4; padding:14px 18px; border-radius:14px; margin-bottom:20px; border:1px solid #dbc4aa; display:flex; justify-content:between; align-items:center;">
            <span style="color:#6b4226; font-weight:bold; font-size:16px;">Koleksi Tersimpan</span>
            <span style="background-color:#a47148; color:white; padding:2px 10px; border-radius:20px; font-size:13px; font-weight:bold;">
                {len(favorites)} Resep
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Membuat Grid Tampilan 2 Kolom
    col1, col2 = st.columns(2)
    grid_columns = [col1, col2]

    for i, recipe_name in enumerate(favorites):
        recipe_data = df[df["Title"] == recipe_name]

        if not recipe_data.empty:
            recipe = recipe_data.iloc[0]
            title = str(recipe["Title"])
            ingredients = [x.strip() for x in str(recipe["Ingredients"]).split("--") if x.strip()]

            # Ambil maksimal 4 bahan untuk preview card
            preview_text = " • ".join(ingredients[:4])
            if len(ingredients) > 4:
                preview_text += " ..."

            with grid_columns[i % 2]:
                # Gunakan satu container utuh tanpa nested border kustom di dalam markdown
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div style="background-color:#fffaf3; padding:5px; border-radius:8px;">
                            <h3 style="color:#6b4226; margin:0 0 10px 0; font-size:20px; font-weight:bold;">{title}</h3>
                            <div style="background-color:#f5ebe0; padding:10px; border-radius:8px; color:#4b3a2f; font-size:13px; margin-bottom:12px; line-height:1.5;">
                                <b>Preview Bahan:</b><br>{preview_text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Expander diletakkan proporsional di dalam container resep
                    with st.expander("Lihat Detail Langkah & Bahan"):
                        st.write("**Bahan Lengkap:**")
                        for ing in ingredients:
                            st.write(f"• {ing}")
                        
                        st.write("---")
                        st.write("**Langkah Memasak:**")
                        steps = str(recipe["Steps"])
                        step_list = steps.split("--") if "--" in steps else steps.split("\n")
                        
                        nomor = 1
                        for step in step_list:
                            step = step.strip()
                            if step:
                                st.write(f"{nomor}. {step}")
                                nomor += 1

                    # Tombol aksi hapus dengan layout penuh mengikuti kontainer kolom
                    if st.button("❌ Hapus dari Favorit", key=f"hapus_{i}", use_container_width=True):
                        st.session_state["favorites"].remove(recipe_name)
                        st.toast(f"{title} berhasil dihapus")
                        st.rerun()