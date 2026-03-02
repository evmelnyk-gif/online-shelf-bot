import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

st.title("Интерактивная полка для ТОП-SKU")

# Инициализация состояния сессии
if "layout_df" not in st.session_state:
    st.session_state.layout_df = pd.DataFrame(columns=["SKU", "Ширина", "Глубина", "Приоритет", "МинФейсинг", "Маржа", "Фейсинг"])

# Загрузка Excel с продуктами
st.sidebar.header("Загрузите Excel с ТОП-SKU")
uploaded_file = st.sidebar.file_uploader("Выберите файл", type=["xlsx", "csv"])

if uploaded_file:
    if uploaded_file.name.endswith(".xlsx"):
        sku_df = pd.read_excel(uploaded_file)
    else:
        sku_df = pd.read_csv(uploaded_file)
    
    st.write("Список ТОП-SKU:")
    st.dataframe(sku_df)

    # Инициализация фейсинга, если ещё пусто
    if st.session_state.layout_df.empty:
        st.session_state.layout_df = sku_df.copy()
        st.session_state.layout_df["Фейсинг"] = st.session_state.layout_df["МинФейсинг"]

    # Ввод размеров полки
    st.sidebar.header("Размеры полки (см)")
    shelf_width = st.sidebar.number_input("Ширина полки", value=100)
    shelf_height = st.sidebar.number_input("Высота полки", value=30)
    shelf_depth = st.sidebar.number_input("Глубина полки", value=25)

    # Интерактивные элементы для каждого SKU
    st.subheader("Редактирование фейсинга и управление SKU")
    for i in range(len(st.session_state.layout_df)):
        row = st.session_state.layout_df.iloc[i]
        col1, col2, col3 = st.columns([3,2,2])
        with col1:
            st.text(row["SKU"])
        with col2:
            new_face = st.number_input(f"Фейсинг {row['SKU']}", min_value=0, value=row["Фейсинг"], key=f"face_{i}")
            st.session_state.layout_df.at[i, "Фейсинг"] = new_face
        with col3:
            if st.button(f"Удалить {row['SKU']}", key=f"del_{i}"):
                st.session_state.layout_df = st.session_state.layout_df.drop(i).reset_index(drop=True)

    # Добавление нового SKU
    st.subheader("Добавить новый SKU")
    new_sku = st.text_input("Название SKU", key="new_sku_name")
    new_width = st.number_input("Ширина", min_value=1, key="new_sku_width")
    new_depth = st.number_input("Глубина", min_value=1, key="new_sku_depth")
    new_priority = st.number_input("Приоритет", min_value=1, max_value=5, value=3, key="new_sku_priority")
    new_minface = st.number_input("МинФейсинг", min_value=0, value=1, key="new_sku_minface")
    new_margin = st.number_input("Маржа", min_value=0.0, value=1.0, key="new_sku_margin")
    if st.button("Добавить SKU"):
        new_row = {"SKU": new_sku, "Ширина": new_width, "Глубина": new_depth, 
                   "Приоритет": new_priority, "МинФейсинг": new_minface, "Маржа": new_margin,
                   "Фейсинг": new_minface}
        st.session_state.layout_df = pd.concat([st.session_state.layout_df, pd.DataFrame([new_row])]).reset_index(drop=True)

    # Визуализация полки
    st.subheader("Визуализация полки")
    fig, ax = plt.subplots(figsize=(12,2))
    current_x = 0
    colors = {}
    for sku in st.session_state.layout_df["SKU"].unique():
        colors[sku] = "#" + "".join([random.choice("0123456789ABCDEF") for _ in range(6)])
    for _, row in st.session_state.layout_df.iterrows():
        width = row["Фейсинг"] * row["Ширина"]
        if current_x + width > shelf_width:
            width = shelf_width - current_x  # не вылезать за полку
        rect = patches.Rectangle((current_x, 0), width, shelf_height, facecolor=colors[row["SKU"]], edgecolor='black')
        ax.add_patch(rect)
        ax.text(current_x + width/2, shelf_height/2, row["SKU"], ha='center', va='center', fontsize=9)
        current_x += width
        if current_x >= shelf_width:
            break

    ax.set_xlim(0, shelf_width)
    ax.set_ylim(0, shelf_height)
    ax.axis('off')
    st.pyplot(fig)

else:
    st.info("Загрузите файл Excel с ТОП-SKU")