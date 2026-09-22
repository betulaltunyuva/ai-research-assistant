import time
from pathlib import Path
import os

import requests
import streamlit as st

from utils.report_exporter import export_report


API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# TASARIM
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    .hero {
        padding: 28px 32px;
        border-radius: 20px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 24px;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.4rem;
    }

    .hero p {
        opacity: 0.75;
        font-size: 1rem;
        margin-top: 8px;
        margin-bottom: 0;
    }

    .feature-badge {
        display: inline-block;
        padding: 6px 11px;
        margin-right: 6px;
        margin-top: 10px;
        border-radius: 20px;
        border: 1px solid rgba(128,128,128,0.30);
        font-size: 0.82rem;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 650;
        margin-bottom: 10px;
    }

    .small-muted {
        opacity: 0.65;
        font-size: 0.9rem;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.25);
        padding: 15px;
        border-radius: 14px;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# API YARDIMCILARI
# ---------------------------------------------------------

def check_api():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=2
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


def get_sessions():
    try:
        response = requests.get(
            f"{API_URL}/sessions",
            timeout=5
        )

        if response.status_code == 200:
            return response.json().get(
                "sessions",
                []
            )

    except requests.RequestException:
        pass

    return []


def get_reports():
    try:
        response = requests.get(
            f"{API_URL}/reports",
            timeout=5
        )

        if response.status_code == 200:
            return response.json().get(
                "reports",
                []
            )

    except requests.RequestException:
        pass

    return []


def upload_document(uploaded_file):
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }

    response = requests.post(
        f"{API_URL}/upload",
        files=files,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            response.text
        )

    return response.json()


def start_research(
    query,
    session_id,
    document_path
):
    payload = {
        "query": query,
        "session_id": session_id,
        "document_path": document_path
    }

    response = requests.post(
        f"{API_URL}/research",
        json=payload,
        timeout=900
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()


def start_research_job(
    query,
    session_id,
    document_path
):
    payload = {
        "query": query,
        "session_id": session_id,
        "document_path": document_path
    }

    response = requests.post(
        f"{API_URL}/research/start",
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()


def get_research_status(
    job_id
):
    response = requests.get(
        f"{API_URL}/research/status/{job_id}",
        timeout=15
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()

AGENT_LABELS = {
    "researcher": "Researcher",
    "analyst": "Analyst",
    "writer": "Writer",
    "verifier": "Verifier"
}



def render_all_agents(
    placeholders,
    agents
):
    for agent_name in AGENT_LABELS:
        render_agent_status(
            placeholders[agent_name],
            agent_name,
            agents.get(
                agent_name,
                "waiting"
            )
        )
    response = requests.get(
        f"{API_URL}/research/status/{job_id}",
        timeout=15
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()
    payload = {
        "query": query,
        "session_id": session_id,
        "document_path": document_path
    }

    response = requests.post(
        f"{API_URL}/research",
        json=payload,
        timeout=900
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()
def get_research_status(
    job_id
):
    response = requests.get(
        f"{API_URL}/research/status/{job_id}",
        timeout=15
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()


AGENT_LABELS = {
    "researcher": "Researcher",
    "analyst": "Analyst",
    "writer": "Writer",
    "verifier": "Verifier"
}


def render_agent_status(
    placeholder,
    agent_name,
    status
):
    label = AGENT_LABELS.get(
        agent_name,
        agent_name
    )

    if status == "running":
        placeholder.warning(
            f"⏳ **{label}** — Çalışıyor"
        )

    elif status == "completed":
        placeholder.success(
            f"✅ **{label}** — Tamamlandı"
        )

    elif status == "failed":
        placeholder.error(
            f"❌ **{label}** — Hata"
        )

    else:
        placeholder.info(
            f"○ **{label}** — Bekliyor"
        )

def render_all_agents(
    placeholders,
    agents
):
    for agent_name in AGENT_LABELS:
        render_agent_status(
            placeholders[agent_name],
            agent_name,
            agents.get(
                agent_name,
                "waiting"
            )
        )


def ask_follow_up(
    question,
    session_id
):
    payload = {
        "question": question,
        "session_id": session_id
    }

    response = requests.post(
        f"{API_URL}/ask",
        json=payload,
        timeout=300
    )

    if response.status_code != 200:
        try:
            detail = response.json().get(
                "detail",
                response.text
            )
        except Exception:
            detail = response.text

        raise RuntimeError(detail)

    return response.json()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "uploaded_document_path" not in st.session_state:
    st.session_state.uploaded_document_path = ""

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "report_exports" not in st.session_state:
    st.session_state.report_exports = None

if "report_export_query" not in st.session_state:
    st.session_state.report_export_query = ""

if "follow_up_answer" not in st.session_state:
    st.session_state.follow_up_answer = None


api_online = check_api()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.title("🔎 AI Research")

    st.caption(
        "Multi-Agent Research Platform"
    )

    st.divider()

    st.subheader("Oturum")

    session_id = st.text_input(
        "Oturum adı",
        value="default",
        placeholder="örnek: network-01"
    )

    if not session_id.strip():
        session_id = "default"

    st.caption(
        "Aynı oturum adı kullanıldığında "
        "önceki araştırma hafızası korunur."
    )

    st.divider()

    st.subheader("Sistem")

    if api_online:
        st.success(
            "FastAPI bağlantısı aktif",
            icon="✅"
        )
    else:
        st.error(
            "FastAPI bağlantısı yok",
            icon="⚠️"
        )

    st.markdown(
        """
        **Altyapı**

        ✓ Multi-Agent  
        ✓ RAG  
        ✓ FAISS  
        ✓ Local Embedding  
        ✓ SQLite Memory  
        ✓ Web Research
        """
    )


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
<div class="hero">
<h1>AI Research Assistant</h1>
<p>Web kaynaklarını ve yüklediğiniz belgeleri birlikte araştıran multi-agent yapay zekâ platformu.</p>
<div>
<span class="feature-badge">Multi-Agent</span>
<span class="feature-badge">Live Web Research</span>
<span class="feature-badge">RAG</span>
<span class="feature-badge">FAISS</span>
<span class="feature-badge">Local AI</span>
<span class="feature-badge">Persistent Memory</span>
</div>
</div>
""",
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

research_tab, sessions_tab, reports_tab = st.tabs(
    [
        "🔎 Araştırma",
        "🧠 Oturumlar",
        "📄 Raporlar"
    ]
)


# =========================================================
# ARAŞTIRMA
# =========================================================

with research_tab:
    document_path = st.session_state.get(
    "uploaded_document_path",
    ""
)

    left_column, right_column = st.columns(
        [2, 1],
        gap="large"
    )
    agent_placeholders = {}


with right_column:

    st.markdown(
        '<div class="section-title">'
        'Araştırma Ayarları'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        f"Aktif oturum: **{session_id}**"
    )

    if document_path:
        st.success(
            "Belge kaynağı aktif"
        )
    else:
        st.caption(
            "Belge eklenmedi. "
            "Araştırma web kaynaklarıyla yapılacak."
        )

    st.divider()

    st.caption(
        "Canlı Agent Durumu"
    )

    for agent_name in AGENT_LABELS:
        agent_placeholders[
            agent_name
        ] = st.empty()

    render_all_agents(
        agent_placeholders,
        {
            "researcher": "waiting",
            "analyst": "waiting",
            "writer": "waiting",
            "verifier": "waiting"
        }
    )

    with left_column:

        st.markdown(
            '<div class="section-title">'
            'Yeni Araştırma'
            '</div>',
            unsafe_allow_html=True
        )

        query = st.text_area(
            "Araştırma konusu",
            height=140,
            placeholder=(
                "Örneğin: "
                "UDP neden bağlantısız çalışır?"
            )
        )

        uploaded_file = st.file_uploader(
            "Belge ekle",
            type=[
                "pdf",
                "docx",
                "txt"
            ],
            help=(
                "İsteğe bağlı. "
                "PDF, DOCX veya TXT yükleyebilirsiniz."
            )
        )

        if uploaded_file is not None:

            if st.button(
                "Belgeyi yükle",
                use_container_width=True
            ):
                if not api_online:
                    st.error(
                        "Önce FastAPI sunucusunu çalıştırın."
                    )

                else:
                    try:
                        with st.spinner(
                            "Belge yükleniyor..."
                        ):
                            upload_result = (
                                upload_document(
                                    uploaded_file
                                )
                            )

                        st.session_state[
                            "uploaded_document_path"
                        ] = upload_result[
                            "file_path"
                        ]

                        st.success(
                            "Belge başarıyla yüklendi."
                        )

                    except Exception as error:
                        st.error(
                            f"Belge yüklenemedi: {error}"
                        )

        document_path = st.session_state.get(
            "uploaded_document_path",
            ""
        )

        if document_path:
            st.info(
                f"Kullanılacak belge: "
                f"{document_path}"
            )

        research_button = st.button(
            "🚀 Araştırmayı Başlat",
            type="primary",
            use_container_width=True
        )

        if research_button:

            if not api_online:
                st.error(
                    "FastAPI sunucusu çalışmıyor."
                )

            elif not query.strip():
                st.warning(
                    "Araştırma konusu yazmalısınız."
                )

            else:
                try:
                    render_all_agents(
                        agent_placeholders,
                        {
                            "researcher": "waiting",
                            "analyst": "waiting",
                            "writer": "waiting",
                            "verifier": "waiting"
                        }
                    )

                    start_result = (
                        start_research_job(
                            query=query.strip(),
                            session_id=session_id,
                            document_path=document_path
                        )
                    )

                    job_id = start_result[
                        "job_id"
                    ]

                    with st.status(
                        "Araştırma yürütülüyor...",
                        expanded=True
                    ) as status_box:

                        st.write(
                            "Multi-agent araştırma başlatıldı."
                        )

                        while True:
                            job = get_research_status(
                                job_id
                            )

                            agent_states = job.get(
                                "agents",
                                {}
                            )

                            render_all_agents(
                                agent_placeholders,
                                agent_states
                            )

                            job_state = job.get(
                                "status"
                            )

                            if job_state == "completed":
                                result = job.get(
                                    "result"
                                )

                                st.session_state[
                                    "research_result"
                                ] = result

                                status_box.update(
                                    label="Araştırma tamamlandı.",
                                    state="complete",
                                    expanded=False
                                )

                                break

                            if job_state == "failed":
                                error_message = (
                                    job.get("error")
                                    or
                                    "Bilinmeyen hata."
                                )

                                status_box.update(
                                    label="Araştırma başarısız.",
                                    state="error",
                                    expanded=True
                                )

                                raise RuntimeError(
                                    error_message
                                )

                            time.sleep(1.5)

                except Exception as error:
                    st.error(
                        f"Araştırma başarısız: {error}"
                    )

    # -----------------------------------------------------
    # ARAŞTIRMA SONUCU
    # -----------------------------------------------------

    result = st.session_state.get(
        "research_result"
    )

    if result:
        current_query = result.get(
            "query",
            "research-report"
        )

        if (
            st.session_state.report_exports is None
            or
            st.session_state.report_export_query
            != current_query
        ):
            st.session_state.report_exports = (
                export_report(
                    query=current_query,
                    final_answer=result.get(
                        "final_answer",
                        ""
                    )
                )
            )

            st.session_state.report_export_query = (
                current_query
            )

        st.divider()

        st.subheader(
            "Araştırma Sonucu"
        )

        metric1, metric2, metric3 = st.columns(
            3
        )

        metric1.metric(
            "Web Kaynağı",
            result.get(
                "source_count",
                0
            )
        )

        metric2.metric(
            "Düzeltme",
            result.get(
                "revision_count",
                0
            )
        )

        metric3.metric(
            "Süre",
            f"{result.get('duration_seconds', 0)} sn"
        )

        report_tab, verify_tab, follow_tab = st.tabs(
            [
                "📝 Nihai Rapor",
                "✅ Doğrulama",
                "💬 Devam Sorusu"
            ]
        )

        with report_tab:

            exports = st.session_state.get(
                "report_exports"
            )

            if exports:

                docx_path = Path(
                    exports["docx_path"]
                )

                pdf_path = Path(
                    exports["pdf_path"]
                )

                download_col1, download_col2 = (
                    st.columns(2)
                )

                if docx_path.exists():
                    with download_col1:
                        st.download_button(
                            label="📄 Word İndir",
                            data=docx_path.read_bytes(),
                            file_name=docx_path.name,
                            mime=(
                                "application/"
                                "vnd.openxmlformats-"
                                "officedocument."
                                "wordprocessingml."
                                "document"
                            ),
                            use_container_width=True
                        )

                if pdf_path.exists():
                    with download_col2:
                        st.download_button(
                            label="📕 PDF İndir",
                            data=pdf_path.read_bytes(),
                            file_name=pdf_path.name,
                            mime="application/pdf",
                            use_container_width=True
                        )

                st.divider()

        st.markdown(
                result.get(
                    "final_answer",
                    "Rapor bulunamadı."
                )
        )

        with verify_tab:

            verification = result.get(
                "verification_report",
                ""
            )

            if (
                "DURUM: UYGUN"
                in verification.upper()
            ):
                st.success(
                    "Doğrulama başarılı"
                )

            else:
                st.warning(
                    "İnsan incelemesi veya "
                    "düzeltme gerekebilir."
                )

            st.text(
                verification
            )

        with follow_tab:

            follow_question = st.text_area(
                "Bu araştırmayla ilgili devam sorusu",
                placeholder=(
                    "Örneğin: Belge kaynağındaki "
                    "kısmı biraz daha açıkla."
                )
            )

            if st.button(
                "Soruyu gönder",
                use_container_width=True
            ):

                if not follow_question.strip():
                    st.warning(
                        "Bir soru yazın."
                    )

                else:
                    try:
                        with st.spinner(
                            "Cevap hazırlanıyor..."
                        ):
                            follow_result = (
                                ask_follow_up(
                                    follow_question.strip(),
                                    session_id
                                )
                            )

                        st.session_state[
                            "follow_up_answer"
                        ] = follow_result.get(
                            "answer",
                            ""
                        )

                    except Exception as error:
                        st.error(
                            f"Soru cevaplanamadı: "
                            f"{error}"
                        )

            follow_answer = st.session_state.get(
                "follow_up_answer"
            )

            if follow_answer:
                st.markdown(
                    "#### Cevap"
                )

                st.write(
                    follow_answer
                )

# =========================================================
# OTURUMLAR
# =========================================================

with sessions_tab:

    st.subheader(
        "Araştırma Oturumları"
    )

    sessions = get_sessions()

    if not sessions:
        st.info(
            "Henüz kayıtlı araştırma oturumu bulunmuyor."
        )

    else:

        for session in sessions:

            with st.container(
                border=True
            ):
                col1, col2, col3 = st.columns(
                    [2, 1, 2]
                )

                col1.markdown(
                    f"**{session.get('session_id')}**"
                )

                col2.metric(
                    "Araştırma",
                    session.get(
                        "research_count",
                        0
                    )
                )

                col3.caption(
                    "Son aktivite: "
                    f"{session.get('last_activity', '-')}"
                )


# =========================================================
# RAPORLAR
# =========================================================

with reports_tab:

    st.subheader(
        "Kaydedilmiş Raporlar"
    )

    reports = get_reports()

    if not reports:
        st.info(
            "Henüz kayıtlı rapor bulunmuyor."
        )

    else:

        for report in reports:

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [4, 1]
                )

                col1.markdown(
                    f"**{report.get('file_name')}**"
                )

                col1.caption(
                    report.get(
                        "file_path",
                        ""
                    )
                )

                col2.metric(
                    "Boyut",
                    f"{report.get('size_bytes', 0)} B"
                )