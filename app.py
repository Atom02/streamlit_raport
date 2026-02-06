import streamlit as st
import pandas as pd
from data_processor import init_db, parse_data, save_to_db, get_all_students, get_student_report, regenerate_token, clear_all_scores

# Page Config
st.set_page_config(page_title="Rapor Siswa", page_icon="📝", layout="centered")

# Initialize DB
init_db()

# --- HELPER FUNCTIONS ---

def admin_view():
    st.title("Dashboard Admin 🔒")
    
    # Base URL configuration
    if "base_url" not in st.session_state:
        st.session_state.base_url = "http://localhost:8501"
        
    base_url = st.text_input("URL Dasar Aplikasi (untuk link)", value=st.session_state.base_url)
    
    # Update session state when input changes
    if base_url != st.session_state.base_url:
        st.session_state.base_url = base_url
    
    
    with st.expander("Upload Data Baru", expanded=True):
        uploaded_file = st.file_uploader("Upload CSV atau Excel", type=['csv', 'xlsx'])
        if uploaded_file is not None:
            try:
                # Show Preview
                df = parse_data(uploaded_file)
                st.write("Pratinjau:", df.head(3))
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Simpan ke Database (Update)"):
                        save_to_db(df)
                        st.success("Data berhasil disimpan!")
                        st.rerun()
                
                with col2:
                    if st.button("⚠️ Hapus Semua Nilai & Simpan", type="primary"):
                        clear_all_scores()
                        save_to_db(df)
                        st.success("Nilai lama dihapus. Data baru disimpan!")
                        st.rerun()

            except Exception as e:
                st.error(f"Gagal memproses file: {e}")

    st.subheader("Kelola Data")
    if st.button("🗑️ Hapus Semua Nilai Saja (Link Tetap Ada)"):
        clear_all_scores()
        st.warning("Semua nilai telah dihapus. Link siswa masih berlaku.")
        st.rerun()

    st.divider()
    
    st.subheader("Link Siswa")
    students = get_all_students()
    
    if not students.empty:
        # Create a display dataframe
        display_data = []
        for index, row in students.iterrows():
            # Combine Base URL with token path
            link = f"{base_url}/?token={row['access_token']}"
            display_data.append({
                "ID": row['id'],
                "Name": row['name'],
                "Link": link,
                "Token": row['access_token']
            })
        
        # We can't put buttons easily in a pure dataframe, so we iterate
        for s in display_data:
            c1, c2, c3 = st.columns([3, 5, 2])
            with c1:
                st.write(f"**{s['Name']}**")
            with c2:
                # st.code provides a copy button automatically (tombol copy ada di pojok kanan atas)
                st.code(s['Link'], language="text")
                st.caption("👆 Klik tombol copy di pojok kanan")
                st.link_button("Buka Link 🔗", s['Link'])
            with c3:
                if st.button("Regenerasi 🔄", key=f"regen_{s['ID']}"):
                    regenerate_token(s['ID'])
                    st.rerun()
            st.divider()
    else:
        st.info("Belum ada siswa. Upload CSV untuk memulai.")

def parent_view(token):
    student, scores, all_subjects = get_student_report(token)
    
    if student is None:
        st.error("Token Tidak Valid atau Kadaluarsa. Silakan hubungi admin sekolah.")
        return

    # -- Report Card Design --
    st.header(f"🎓 Rapor: {student['name']}")
    st.caption(f"ID Siswa: {student['original_id']}")
    st.divider()

    # Pivot scores: Subject as rows, Types as columns
    if not scores.empty:
        pivot_df = scores.pivot(index='subject', columns='score_type', values='score')
    else:
        pivot_df = pd.DataFrame()

    # Ensure all subjects are present
    if all_subjects:
        # Reindex to include all known subjects
        pivot_df = pivot_df.reindex(all_subjects)
    
    # Handling Empty Data
    if pivot_df.empty:
        st.warning("Belum ada data nilai sama sekali.")
        return

    # Calculate Average (only for valid numbers)
    pivot_df['Rata-rata'] = pivot_df.mean(axis=1)
    
    # Fill NaN with specific placeholder string?
    # Dataframes with mixed types (float + string) are tricky for styling.
    # Approach: Convert to string, format numbers, then fillna.
    
    # 1. Format numbers to string with 1 decimal
    display_df = pivot_df.copy()
    
    # Apply number formatting only to numeric columns
    for col in display_df.columns:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.1f}" if pd.notnull(x) else x)
    
    # 2. Fill NaN
    display_df = display_df.fillna("Belum ada data")
    
    # Styling
    # We can't use background_gradient easily on strings. 
    # We will fallback to simple table for mixed content or use applymap for styling.
    
    def highlight_empty(val):
        color = 'color: #ffcccc' if val == "Belum ada data" else ''
        return color

    st.dataframe(
        display_df.style.map(highlight_empty),
        use_container_width=True
    )

    # Charts (Need numeric data, drop NaNs)
    st.subheader("Ringkasan Performa")
    valid_scores = pivot_df['Rata-rata'].dropna()
    if not valid_scores.empty:
        st.bar_chart(valid_scores)
    else:
        st.info("Grafik tidak tersedia karena belum ada nilai.")

# --- MAIN ROUTING ---

# Check query params
query_params = st.query_params
token = query_params.get("token", None)

if token:
    parent_view(token)
else:
    # Admin Login simulation (Sidebar)
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        with st.sidebar:
            st.header("Akses Admin")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if password == "dedePetot!": # Simple hardcoded password
                    st.session_state.admin_logged_in = True
                    st.rerun()
                elif password:
                    st.error("Password Admin salah.")
    else:
        with st.sidebar:
            st.header(f"Admin Logged In")
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.rerun()
        
        admin_view()

