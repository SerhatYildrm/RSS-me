
import streamlit as st
import feedparser
from datetime import datetime, timezone
import source

import schedule


st.balloons()

# TODAY
today = datetime.today().strftime("%d.%m.%y")

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


schedule.every(1).minutes.do(get_data)

with st.spinner(text="Rss kaynakları sorgulanıyor..."):
    database = get_data()

with st.sidebar:
    st.write(f":bird: <h1> RSS Me</h1>",unsafe_allow_html=True)
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
    _db.add_rss(new_rss, new_rss_url)
    st.cache_data.clear()
    st.experimental_rerun()

if today_publish:
    st.write(f"<h1>Bugün Yayınlananlar</h1>",unsafe_allow_html=True)
    st.write("<hr />",unsafe_allow_html=True)
    for key in database.keys():
        for entry in database.get(key).entries:
            if(entry.has_key("published_parsed")):
                entry_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
            else:
                entry_time = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
            
            if today == entry_time:
                st.write(f"<span style='color: red;'>[{entry_time}]</span>  site: {key} - {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a> :open_book:", unsafe_allow_html= True)
else:
    if search_in_rss != '':
        st.write(f"<h1>Aranan : {search_in_rss}</h1>",unsafe_allow_html=True)
        st.write("<hr />",unsafe_allow_html=True)

        for key in database.keys():
            for entry in database.get(key).entries:
                if entry.has_key("summary_detail"):
                    if search_in_rss.lower() in entry.summary_detail.value.lower():
                        if(entry.has_key("published_parsed")):
                            entry_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
                        else:
                            entry_time = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
                        st.write(f"<span style='color: red;'>[{entry_time}]</span>  site: {key} - {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a>", unsafe_allow_html= True)
                else:
                    st.write("Birşey bulunamadı ... :eyes:")
                    break
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"<h1>{selected_rss}</h1>",unsafe_allow_html=True)
        with col2:
            delete = st.button("Sil")
            if delete:
                _db.delete_rss(selected_rss)
                st.cache_data.clear()
                st.experimental_rerun()

        st.write("<hr />",unsafe_allow_html=True)
        for entry in used_rss.entries:
            if(entry.has_key("published_parsed")):
                entry_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
            else:
                entry_time = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc).strftime("%d.%m.%y")
            if today == entry_time:
                st.write(f"<span style='color: green;'>[BUGÜN YAZILDI]</span> {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a>", unsafe_allow_html= True)
            else:
                st.write(f"<span style='color: red;'>[{entry_time}]</span>  {entry.title} - <a  href='{entry.link}' target='_blank'>oku</a>", unsafe_allow_html= True)









