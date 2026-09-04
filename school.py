import re
import time
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.set_page_config(
    page_title="HK University Jobs",
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

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

HKU_LIST_URL = "https://jobs.hku.hk/en/listing/"


def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


@st.cache_data(ttl=3600, show_spinner=False)
def get_hku_jobs():
    response = requests.get(HKU_LIST_URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    for row in soup.select("table tbody tr"):
        cells = row.find_all("td")

        if len(cells) < 4:
            continue

        link = row.find("a")

        if not link or not link.get("href"):
            continue

        title = clean_text(link.get_text(" ", strip=True))
        job_url = urljoin(HKU_LIST_URL, link["href"])
        department = clean_text(cells[2].get_text(" ", strip=True))
        closing_date = clean_text(cells[3].get_text(" ", strip=True))

        jobs.append({
            "university": "The University of Hong Kong (HKU)",
            "title": title,
            "department": department,
            "closing_date": closing_date,
            "url": job_url
        })

    unique_jobs = {job["url"]: job for job in jobs}
    return list(unique_jobs.values())


@st.cache_data(ttl=3600, show_spinner=False)
def get_job_jd(job_url):
    response = requests.get(job_url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    return clean_text(soup.get_text(" ", strip=True))


def matched_keywords(job, keywords):
    searchable_text = (
        f"{job['title']} "
        f"{job['department']} "
        f"{job.get('jd', '')}"
    ).lower()

    return [
        keyword
        for keyword in keywords
        if keyword in searchable_text
    ]


st.title("💼 HKU 真实招聘职位匹配")
st.write("系统会根据职位名称、部门和职位详情（JD）匹配你的技能。")

user_input = st.text_input(
    "输入你的技能或目标岗位",
    placeholder="例如：python, SPSS, research, data analysis"
)

st.caption("请输入英文关键词，并用英文逗号分隔。例如：python, research, data")

try:
    jobs = get_hku_jobs()
    st.success(f"已读取 HKU {len(jobs)} 个真实职位。")
except Exception:
    jobs = []
    st.error("暂时无法读取 HKU 职位网页，请稍后刷新。")

if user_input and jobs:
    keywords = [
        word.strip().lower()
        for word in user_input.replace("，", ",").split(",")
        if word.strip()
    ]

    st.info("正在读取职位详情和 JD，请稍等。第一次运行可能需要约 1 分钟。")

    results = []
    progress_bar = st.progress(0)

    for i, job in enumerate(jobs):
        try:
            job["jd"] = get_job_jd(job["url"])
            matches = matched_keywords(job, keywords)

            if matches:
                job["matched_keywords"] = matches
                job["score"] = len(matches)
                results.append(job)

        except Exception:
            pass

        progress_bar.progress((i + 1) / len(jobs))
        time.sleep(0.05)

    progress_bar.empty()

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.divider()
    st.subheader("匹配到的真实职位")

    if results:
        for job in results:
            jd_preview = job["jd"][:500] + "..." if len(job["jd"]) > 500 else job["jd"]

            st.markdown(f"""
            <div class="job-card">
                <b>{job["title"]}</b><br>
                学校：{job["university"]}<br>
                部门：{job["department"]}<br>
                匹配关键词：{", ".join(job["matched_keywords"])}<br>
                截止日期：{job["closing_date"]}<br><br>
                <b>JD 摘要：</b><br>
                {jd_preview}
            </div>
            """, unsafe_allow_html=True)

            st.link_button(
                "查看官方职位详情 / 申请",
                job["url"],
                use_container_width=True
            )

    else:
        st.info("没有在职位名称、部门或 JD 中找到你输入的关键词。可以尝试更短的英文词，例如：python、data、research、assistant、teaching。")

elif jobs:
    st.info("请先输入技能或目标岗位。系统将从职位名称、部门和完整 JD 中进行匹配。")
    st.link_button(
        "查看 HKU 官方职位列表",
        HKU_LIST_URL,
        use_container_width=True
    )
