import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shelf Bot", layout="wide")

st.title("🛒 Shelf Chat-Bot")

# Загружаем справочник SKU
@st.cache_data
def load_sku():
    return pd.read_excel("top_sku_example.xlsx")

reference_df = load_sku()

# Создаём "полку" в сессии
if "layout_df" not in st.session_state:
    st.session_state.layout_df = pd.DataFrame(columns=reference_df.columns)

# --- Чат-подобный ввод ---
st.subheader("Добавить SKU")
sku_input = st.text_input("Название SKU")
face_input = st.number_input("Фейсинг", min_value=1, value=1, step=1)

if st.button("Добавить"):
    if sku_input in reference_df["SKU"].values:
        sku_row = reference_df[reference_df["SKU"] == sku_input].copy()
        sku_row["Фейсинг"] = face_input
        st.session_state.layout_df = pd.concat([st.session_state.layout_df, sku_row]).reset_index(drop=True)
        st.success(f"Добавлено {sku_input} с фейсингом {face_input}")
    else:
        st.error("SKU не найден в справочнике!")

# --- Таблица текущей полки ---
st.subheader("Текущая выкладка")
st.dataframe(st.session_state.layout_df)

# --- Удаление SKU ---
st.subheader("Удалить SKU")
delete_input = st.text_input("Название SKU для удаления")
if st.button("Удалить"):
    before_count = len(st.session_state.layout_df)
    st.session_state.layout_df = st.session_state.layout_df[st.session_state.layout_df["SKU"] != delete_input]
    after_count = len(st.session_state.layout_df)
    if before_count != after_count:
        st.success(f"Удалено {delete_input}")
    else:
        st.warning("SKU не найдено в полке")