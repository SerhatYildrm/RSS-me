
import streamlit as st
import feedparser
from datetime import datetime, timezone
from streamlit_modal import Modal
import source

#database = {}

# TODAY
today = datetime.today().strftime("%d.%m.%y")

# rss_source = [
#     {"name" : "Mert Sarıca", "link" : "https://www.mertsarica.com/feed/"},
#     {"name" : "kienmanowar", "link" : "https://kienmanowar.wordpress.com/feed/"},
#     {"name" : "Der Flounder", "link" : "https://derflounder.wordpress.com/feed/"},
#     {"name" : "Misaki's Blog", "link" : "https://misakikata.github.io/atom.xml"},
#     {"name" : "Bleeping Computer", "link" : "https://www.bleepingcomputer.com/feed/"},
#     {"name" : "Teknopat", "link" : "https://www.technopat.net/feed/"},
#     {"name" : "Darkreader", "link" : "https://www.darkreading.com/rss.xml"},
#     {"name" : "Hacker news", "link" : "https://news.ycombinator.com/rss"},
#     {"name" : "Python", "link" : "https://blog.python.org/feeds/posts/default?alt=rss"},
#     {"name" : "Real Python", "link": "https://realpython.com/atom.xml"},
# ]



_db = source.RSSource()

rss_source = _db.load()


st.markdown(""" 
    <style>
        div.stButton > button {
            background-color: #25E795;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(max_entries=10)
def get_data():
    _db = {}
    for rss in rss_source:
        _db.setdefault(rss["name"], feedparser.parse(rss["link"]))
    return _db


with st.spinner(text="Rss kaynakları sorgulanıyor..."):
    database = get_data()

with st.sidebar:
    st.write(f"<h1>RSS Me</h1>",unsafe_allow_html=True)
    st.write("<hr />", unsafe_allow_html= True)
    selected_rss = st.selectbox(" Rss Kaynağı Seç :  ", database.keys())
    st.write("<hr />", unsafe_allow_html= True)
    search_in_rss = st.text_input(" Rss'de ara : ")
    st.write("<hr />", unsafe_allow_html= True)
    today_publish = st.button("Bugün yayınlananları getir.")
    st.write("<hr />", unsafe_allow_html= True)
    new_rss = st.text_input("Kaynak Adı")
    new_rss_url = st.text_input("Kaynak Adresi")
    create_rss = st.button("Yeni kaynak ekle")

used_rss = database.get(selected_rss)

if create_rss:
    print("geldim")
    _db.add_rss(new_rss, new_rss_url)
    st.experimental_rerun()

if today_publish:
    st.write(f"<h1>Bugün Yayınlananlar</h1>",unsafe_allow_html=True)
    st.write("<hr />",unsafe_allow_html=True)
    for key in database.keys():
        for entry in database.get(key).entries:
            entry_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
            
            if today == entry_time:
                st.write(f"<span style='color: red;'>[{entry_time}]</span>  site: {key} - {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a>", unsafe_allow_html= True)
else:
    if search_in_rss != '':
        st.write(f"<h1>Aranan : {search_in_rss}</h1>",unsafe_allow_html=True)
        st.write("<hr />",unsafe_allow_html=True)

        for key in database.keys():
            for entry in database.get(key).entries:
                if search_in_rss.lower() in entry.summary_detail.value.lower():
                    entry_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
                    st.write(f"<span style='color: red;'>[{entry_time}]</span>  site: {key} - {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a>", unsafe_allow_html= True)
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"<h1>{selected_rss}</h1>",unsafe_allow_html=True)
        with col2:
            delete = st.button("Sil")
            if delete:
                _db.delete_rss(selected_rss)

        st.write("<hr />",unsafe_allow_html=True)
        for entry in used_rss.entries:
            entry_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
            if today == entry_time:
                st.write(f"<span style='color: green;'>[BUGÜN YAZILDI]</span> {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a>", unsafe_allow_html= True)
            else:
                st.write(f"<span style='color: red;'>[{entry_time}]</span>  {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a>", unsafe_allow_html= True)









