import streamlit as st
from tmdb import get_genres, discover_movies, search_movies, trending, poster_url

st.set_page_config(page_title="movbul — TMDb", page_icon="🎬", layout="wide")

st.title("🎬 movbul — Movie Recommendation App")
st.caption("Veri kaynağı: The Movie Database (TMDb).")

with st.sidebar:
    st.header("Tercihler")
    query = st.text_input("Film ara (başlık):", placeholder="Alien, Blade Runner, …")
    genres = get_genres()
    genre_map = {g["name"]: g["id"] for g in genres}
    selected = st.multiselect("Tür seç:", list(genre_map.keys()))
    sort = st.selectbox("Sırala:", [
        "vote_average.desc",
        "popularity.desc",
        "release_date.desc"
    ])
    min_votes = st.slider("Min. oy sayısı", 0, 2000, 200, 50)
    section = st.radio("Bölüm:", ["Öneriler", "Trend"], horizontal=True)

def render_cards(items, title):
    st.subheader(title)
    cols = st.columns(5)
    for i, m in enumerate(items):
        with cols[i % 5]:
            p = poster_url(m.get("poster_path"), "w342")
            if p:
                st.image(p, use_container_width=True)
            name = m.get("title") or m.get("name")
            rating = m.get("vote_average", 0)
            year = (m.get("release_date") or "")[:4]
            st.markdown(f"**{name}**  \n⭐ {rating:.1f}  \n📅 {year}")
            st.caption(m.get("overview", "")[:160] + "…")

# Veri çek
if query:
    data = search_movies(query, page=1)
    render_cards(data.get("results", [])[:15], f"🔎 Arama: {query}")
else:
    if section == "Trend":
        data = trending("week", page=1)
        render_cards(data.get("results", [])[:15], "🔥 Haftanın Trendleri")
    else:
        ids = [genre_map[g] for g in selected] if selected else None
        data = discover_movies(genre_ids=ids, sort_by=sort, page=1, min_votes=min_votes)
        render_cards(data.get("results", [])[:15], "🎯 Tercihlere Göre Öneriler")

st.markdown("---")
st.caption("Bu ürün TMDb'yi kullanır ancak TMDb tarafından onaylanmamıştır veya bağlantılı değildir.")
