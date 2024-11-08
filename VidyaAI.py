import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Welcome to VidyaAI",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .section {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid #ddd;
    }
    .emoji {
        font-size: 50px;
        margin-bottom: 10px;
    }
    .title {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        display: block;
        margin-bottom: 5px;
    }
    .description {
        font-size: 18px;
        color: #555;
        margin-bottom: 10px;
    }
    .arrow {
        font-size: 30px;
        color: #007bff;
        text-decoration: none;
    }
    .arrow:hover {
        text-decoration: underline;
    }
    .footer {
        margin-top: 50px;
        text-align: center;
        font-size: 14px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header section
st.title("🎓 Welcome to VidyaAI India")
st.subheader("Empower your career with the right skills!")
st.markdown("Explore our interactive tools and resources below to enhance your skills and prepare for the future!!")

# Feature sections with descriptions and links
st.markdown("## 🔍 Features")

sections = [
    ("📊", "Personalized Job Demand Analyser", "Analyze job trends and receive insights into high-demand skills and career paths.", "https://jobdemandnits.streamlit.app/"),
    ("🎥", "YouTube Video Summarizer & Notes Creator", "Summarize YouTube videos and extract key notes for efficient learning.", "https://videosummarizernits.streamlit.app/")
]

for emoji, title, description, link in sections:
    st.markdown(f"""
    <div class="section">
        <div class="emoji">{emoji}</div>
        <div class="title">{title}</div>
        <div class="description">{description}</div>
        <a href="{link}" target="_blank" class="arrow">➡️</a>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Team: Init_to_Winit<br>
    Team Members: Sayli, Ratan, Bharath
</div>
""", unsafe_allow_html=True)
