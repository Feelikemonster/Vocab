import pandas as pd
import streamlit as st

st.set_page_config(page_title="My Vocab Dictionary", page_icon="📚", layout="centered")

st.title("📚 My Vocab Dictionary")

with st.expander("📱 Telefona uygulama gibi ekle"):
    st.markdown("""
**Android (Chrome):** ⋮ → **Ana ekrana ekle**  
**iPhone (Safari):** Paylaş (⬆️) → **Ana Ekrana Ekle**
""")

st.caption("Her öğrenci kendi sözlüğünü oluşturur. Kapatınca kaybolmaması için CSV indirip sonra tekrar yükleyebilirsin.")

# ---------- Helpers ----------
def normalize_text(s: str) -> str:
    return str(s).strip()

def ensure_df():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["Word (EN)", "Meaning (TR)"])

ensure_df()

# ---------- Import / Export ----------
st.subheader("📥 / 📤 Sözlüğünü Kaydet & Devam Et")

colA, colB = st.columns(2)

with colA:
    uploaded = st.file_uploader("Önceden indirdiğin CSV dosyanı yükle", type=["csv"])
    if uploaded is not None:
        try:
            df_in = pd.read_csv(uploaded)
            # Eski/yanlış kolon adlarını da tolere edelim:
            possible_cols = df_in.columns.tolist()
            if "Word (EN)" not in possible_cols or "Meaning (TR)" not in possible_cols:
                # Kullanıcı farklı başlıklarla yüklediyse yakalamaya çalış
                rename_map = {}
                for c in possible_cols:
                    lc = c.lower()
                    if "word" in lc or "en" in lc:
                        rename_map[c] = "Word (EN)"
                    if "meaning" in lc or "tr" in lc or "turk" in lc or "anlam" in lc:
                        rename_map[c] = "Meaning (TR)"
                df_in = df_in.rename(columns=rename_map)

            df_in = df_in[["Word (EN)", "Meaning (TR)"]].dropna()
            df_in["Word (EN)"] = df_in["Word (EN)"].astype(str).str.strip()
            df_in["Meaning (TR)"] = df_in["Meaning (TR)"].astype(str).str.strip()
            df_in = df_in[(df_in["Word (EN)"] != "") & (df_in["Meaning (TR)"] != "")]

            st.session_state.df = df_in.drop_duplicates().reset_index(drop=True)
            st.success("Sözlük yüklendi ✅")
        except Exception as e:
            st.error("CSV okunamadı. Lütfen uygulamanın indirdiği CSV’yi yükle.")
            st.code(str(e))

with colB:
    csv_bytes = st.session_state.df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Sözlüğümü indir (CSV)",
        data=csv_bytes,
        file_name="my_vocab_dictionary.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# ---------- Add new word ----------
st.subheader("➕ Yeni kelime ekle")

with st.form("add_word_form", clear_on_submit=True):
    en = st.text_input("English word", placeholder="e.g., improve")
    tr = st.text_input("Türkçe anlamı", placeholder="örn. geliştirmek")
    submitted = st.form_submit_button("Ekle")

if submitted:
    en = normalize_text(en)
    tr = normalize_text(tr)

    if not en or not tr:
        st.warning("İki alanı da doldur 🙂")
    else:
        new_row = pd.DataFrame([{"Word (EN)": en, "Meaning (TR)": tr}])
        st.session_state.df = (
            pd.concat([st.session_state.df, new_row], ignore_index=True)
            .drop_duplicates()
            .reset_index(drop=True)
        )
        st.success(f"Eklendi: **{en}** → **{tr}**")

st.divider()

# ---------- Search ----------
st.subheader("🔎 Ara (EN veya TR)")
query = st.text_input("Arama", placeholder="Kelime ya da Türkçe anlam yaz...").strip().lower()

df = st.session_state.df.copy()

if query:
    mask = (
        df["Word (EN)"].astype(str).str.lower().str.contains(query, na=False)
        | df["Meaning (TR)"].astype(str).str.lower().str.contains(query, na=False)
    )
    df_view = df[mask].reset_index(drop=True)
else:
    df_view = df.reset_index(drop=True)

# ---------- Display & edit ----------
st.write(f"Toplam kelime: **{len(st.session_state.df)}** | Görünen: **{len(df_view)}**")

st.dataframe(df_view, use_container_width=True, hide_index=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🧹 Tüm sözlüğü temizle", use_container_width=True):
        st.session_state.df = pd.DataFrame(columns=["Word (EN)", "Meaning (TR)"])
        st.success("Sözlük temizlendi.")

with col2:
    st.info("İpucu: Kapatmadan önce **CSV indir** de. Sonraki girişte **CSV yükle** ile devam et.")
