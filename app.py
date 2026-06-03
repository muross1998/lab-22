import streamlit as st
import folium
from streamlit_folium import st_folium

# Налаштування сторінки Streamlit
st.set_page_config(page_title="Карта Прикарпаття", layout="wide", page_icon="🗺️")

st.title("🏔️ Інтерактивна туристична карта")
st.write("Використовуйте бокове меню, щоб відфільтрувати локації на карті.")

# УДОСКОНАЛЕННЯ: Використовуємо статичні координати для 100% надійності та миттєвого завантаження
locations_data = {
    "Районні центри": {
        "color": "blue",
        "icon": "info-sign",
        "places": {
            "Івано-Франківськ": [48.9226, 24.7111],
            "Калуш": [49.0275, 24.3644],
            "Коломия": [48.5280, 25.0400],
            "Надвірна": [48.6293, 24.5794]
        }
    },
    "Гірські маршрути": {
        "color": "green",
        "icon": "leaf",
        "places": {
            "гора Говерла": [48.1602, 24.5000],
            "гора Петрос": [48.1722, 24.4286],
            "гора Хом'як": [48.3647, 24.4994]
        }
    },
    "Озера": {
        "color": "lightblue",
        "icon": "tint",
        "places": {
            "озеро Росохан": [48.6655, 23.9161],
            "озеро Несамовите": [48.1311, 24.5322]
        }
    }
}

# Інтерактивне меню керування шарами
st.sidebar.header("Налаштування карти")
selected_categories = st.sidebar.multiselect(
    "Оберіть категорії для відображення:",
    options=list(locations_data.keys()),
    default=["Районні центри", "Гірські маршрути"] # Що показувати при запуску
)

# Створення базової карти (центруємо на Івано-Франківщині)
m = folium.Map(location=[48.6, 24.5], zoom_start=8)

# Додавання точок залежно від вибору користувача
for cat in selected_categories:
    data = locations_data[cat]
    fg = folium.FeatureGroup(name=cat).add_to(m)
    
    # Тепер беремо і назву, і координати прямо з нашого словника
    for place, coords in data["places"].items():
        folium.Marker(
            location=coords,
            popup=folium.Popup(place, max_width=200),
            icon=folium.Icon(color=data["color"], icon=data["icon"])
        ).add_to(fg)

# Додаємо вбудований перемикач шарів Folium
folium.LayerControl().add_to(m)

# Відображення карти у Streamlit
st_folium(m, width=1000, height=600)
