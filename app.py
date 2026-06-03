import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Карта Прикарпаття", layout="wide", page_icon="🗺️")

st.title("🏔️ Інтерактивна туристична карта")
st.write("Використовуйте бокове меню, щоб відфільтрувати локації на карті.")

# УДОСКОНАЛЕННЯ 1: Кешування запитів.
# Geopy працює через інтернет і може довго шукати координати. 
# st.cache_data запам'ятовує результати, щоб при кліках карта оновлювалась миттєво.
@st.cache_data
def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="my_tourist_map_app")
    try:
        location = geolocator.geocode(place_name)
        if location:
            return (location.latitude, location.longitude)
    except:
        return None
    return None


locations_data = {
    "Районні центри": {
        "places": ["Івано-Франківськ", "Калуш", "Коломия", "Надвірна"],
        "color": "blue",
        "icon": "info-sign"
    },
    "Гірські маршрути": {
        "places": ["гора Говерла", "гора Петрос", "гора Хом'як"],
        "color": "green",
        "icon": "leaf"
    },
    "Озера": {
        "places": ["озеро Росохан", "озеро Несамовите"],
        "color": "lightblue",
        "icon": "tint"
    }
}


st.sidebar.header("Налаштування карти")
selected_categories = st.sidebar.multiselect(
    "Оберіть категорії для відображення:",
    options=list(locations_data.keys()),
    default=["Районні центри", "Гірські маршрути"] 
)


m = folium.Map(location=[48.6, 24.5], zoom_start=8)

# Додавання точок залежно від вибору користувача
for cat in selected_categories:
    data = locations_data[cat]
    # Створюємо групу для кожної категорії
    fg = folium.FeatureGroup(name=cat).add_to(m)
    
    for place in data["places"]:
        coords = get_coordinates(place)
        if coords:
            folium.Marker(
                location=coords,
                popup=folium.Popup(place, max_width=200),
                icon=folium.Icon(color=data["color"], icon=data["icon"])
            ).add_to(fg)

# Додаємо вбудований перемикач шарів Folium
folium.LayerControl().add_to(m)

# Відображення карти у Streamlit
st_folium(m, width=1000, height=600)
