import streamlit as st

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
    font-size: 26px !important;
}

h2, h3 {
    font-size: 18px !important;
}

.stButton button, .stLinkButton a {
    font-size: 14px !important;
}

.job-card {
    border: 1px solid #dddddd;
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 12px;
    background-color: #fafafa;
}
</style>
""", unsafe_allow_html=True)

universities = [
    {
        "name": "The University of Hong Kong (HKU)",
        "keywords": ["research", "education", "data", "python", "ai", "teaching", "administration"],
        "url": "https://jobs.hku.hk/en/listing/"
    },
    {
        "name": "The Chinese University of Hong Kong (CUHK)",
        "keywords": ["research", "education", "data", "python", "ai", "teaching", "administration"],
        "url": "https://career.cuhk.edu.hk/"
    },
    {
        "name": "Hong Kong University of Science and Technology (HKUST)",
        "keywords": ["research", "science", "engineering", "data", "python", "ai", "technology"],
        "url": "https://hkust.edu.hk/careers"
    },
    {
        "name": "The Hong Kong Polytechnic University (PolyU)",
        "keywords": ["research", "engineering", "design", "data", "technology", "administration"],
        "url": "https://www.polyu.edu.hk/hro/job-vacancies/"
    },
    {
        "name": "City University of Hong Kong (CityUHK)",
        "keywords": ["research", "data", "business", "law", "technology", "engineering", "administration"],
        "url": "https://www.cityu.edu.hk/hro/en/job/current"
    },
    {
        "name": "Hong Kong Baptist University (HKBU)",
        "keywords": ["research", "education", "communication", "media", "data", "teaching", "administration"],
        "url": "https://hro.hkbu.edu.hk/en/career-opportunities"
    },
    {
        "name": "Lingnan University (LU)",
        "keywords": ["research", "education", "social science", "data", "teaching", "administration"],
        "url": "https://www.ln.edu.hk/hr/career"
    },
    {
        "name": "The Education University of Hong Kong (EdUHK)",
        "keywords": ["education", "teaching", "research", "data", "psychology", "social science", "administration"],
        "url": "https://www.eduhk.hk/hro/en/career-opportunities"
    }
]

st.title("💼 香港八大院校招聘职位")
st.write("输入你的技能或目标岗位，小程序会推荐较相关的大学招聘入口。")

user_input = st.text_input(
    "输入关键词，例如：Python、research、data analysis、education、teaching",
    placeholder="例如：Python, research, data analysis"
)

user_keywords = [
    word.strip().lower()
    for word in user_input.replace("，", ",").split(",")
    if word.strip()
]

st.divider()

if user_keywords:
    st.subheader("匹配结果")

    results = []

    for university in universities:
        matched = []

        for keyword in user_keywords:
            for university_keyword in university["keywords"]:
                if keyword in university_keyword or university_keyword in keyword:
                    matched.append(keyword)
                    break

        score = len(set(matched))

        if score > 0:
            results.append({
                "name": university["name"],
                "url": university["url"],
                "matched": list(set(matched)),
                "score": score
            })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    if results:
        for result in results:
            st.markdown(f"""
            <div class="job-card">
                <b>{result["name"]}</b><br>
                匹配关键词：{", ".join(result["matched"])}<br>
                匹配数量：{result["score"]}
            </div>
            """, unsafe_allow_html=True)

            st.link_button(
                f"查看 {result['name']} 官方职位",
                result["url"],
                use_container_width=True
            )
    else:
        st.info("暂时没有找到直接匹配的学校。你可以尝试输入：research、education、data、Python、AI、teaching、administration。")

else:
    st.subheader("全部大学招聘入口")

    for university in universities:
        st.markdown(f"""
        <div class="job-card">
            <b>{university["name"]}</b><br>
            常见相关方向：{", ".join(university["keywords"])}
        </div>
        """, unsafe_allow_html=True)

        st.link_button(
            f"查看 {university['name']} 官方职位",
            university["url"],
            use_container_width=True
        )