import streamlit as st

st.set_page_config(page_title="HK University Jobs", page_icon="💼")

st.title("香港大学招聘职位")
st.write("点击学校名称，前往官方招聘网站查看最新职位。")

jobs_sites = {
    "香港都会大学 HKMU": (
        "Taleo",
        "https://hkmu.taleo.net/careersection/ex_full_time/jobsearch.ftl?lang=en&portal=101430233"
    ),
    "岭南大学 Lingnan University": (
        "Official Career Page",
        "https://www.ln.edu.hk/hr/career"
    )
}

for university, (system, url) in jobs_sites.items():
    st.subheader(university)
    st.caption(f"招聘系统：{system}")
    st.link_button("查看官方职位", url, use_container_width=True)