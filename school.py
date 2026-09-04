import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.set_page_config(
    page_title="Hong Kong University Jobs",
    page_icon="💼",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 14px !important;
}
h1 {
    font-size: 24px !important;
}
h2, h3 {
    font-size: 18px !important;
}
.job-card {
    border: 1px solid #dddddd;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
    background-color: #fafafa;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def get_hku_jobs():
    url = "https://jobs.hku.hk/en/listing/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    for row in soup.select("table tbody tr"):
        cells = row.find_all("td")

        if len(cells) < 4:
            continue

        link = row.find("a")

        if not link:
            continue

        title = link.get_text(" ", strip=True)
        job_url = urljoin(url, link.get("href"))
        department = cells[2].get_text(" ", strip=True)
        closing_date = cells[3].get_text(" ", strip=True)

        if title:
            jobs.append({
                "university": "The University of Hong Kong (HKU)",
                "title": title,
                "department": department,
                "closing_date": closing_date,
                "url": job_url
            })

    unique_jobs = {}

    for job in jobs:
        unique_jobs[job["url"]] = job

    return list(unique_jobs.values())


st.title("💼 香港大学真实招聘职位")
st.write("目前先读取 HKU 官方公开职位。输入技能或岗位关键词，系统会从真实职位名称和部门中寻找相关职位。")

user_input = st.text_input(
    "输入你的技能或目标岗位",
    placeholder="例如：python, research, data, education"
)

st.caption("提示：目前是关键词匹配，不是 AI 判断。输入越具体，结果越准确。")

try:
    jobs = get_hku_jobs()
except Exception:
    jobs = []
    st.error("暂时无法读取 HKU 职位网页，请稍后刷新。")

if jobs:
    st.success(f"已读取 HKU {len(jobs)} 个真实职位。")
else:
    st.warning("暂时未能读取职位。你仍可到 HKU 官网查看。")
    st.link_button(
        "打开 HKU 官方职位网页",
        "https://jobs.hku.hk/en/listing/"
    )

if user_input and jobs:
    keywords = [
        word.strip().lower()
        for word in user_input.replace("，", ",").split(",")
        if word.strip()
    ]

    results = []

    for job in jobs:
        job_text = f"{job['title']} {job['department']}".lower()

        matched_keywords = [
            keyword for keyword in keywords
            if keyword in job_text
        ]

        if matched_keywords:
            job["matched_keywords"] = matched_keywords
            job["score"] = len(matched_keywords)
            results.append(job)

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.divider()
    st.subheader("匹配到的真实职位")

    if results:
        for job in results:
            closing = job["closing_date"] if job["closing_date"] else "请到官网查看"

            st.markdown(f"""
            <div class="job-card">
                <b>{job["title"]}</b><br>
                学校：{job["university"]}<br>
                部门：{job["department"]}<br>
                匹配关键词：{", ".join(job["matched_keywords"])}<br>
                截止日期：{closing}
            </div>
            """, unsafe_allow_html=True)

            st.link_button(
                "查看职位详情 / 去官网申请",
                job["url"],
                use_container_width=True
            )
    else:
        st.info("没有在 HKU 当前职位标题或部门名称中找到这些关键词。可尝试：research、assistant、lecturer、data、software、education、administration。")

elif jobs:
    st.divider()
    st.subheader("HKU 当前职位（前 30 个）")

    for job in jobs[:30]:
        closing = job["closing_date"] if job["closing_date"] else "请到官网查看"

        st.markdown(f"""
        <div class="job-card">
            <b>{job["title"]}</b><br>
            部门：{job["department"]}<br>
            截止日期：{closing}
        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            "查看职位详情",
            job["url"],
            use_container_width=True
        )
