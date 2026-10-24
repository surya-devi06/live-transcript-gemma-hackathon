"""Live Transcript AI - Main Streamlit Application."""

import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from src.transcriber import AudioTranscriber, TranscriptionResult
from src.gemma_client import GemmaClient
from src.notes_generator import NotesGenerator
from src.qa_engine import QAEngine
from src.export_utils import ExportManager

# Load local environment configuration
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Live Transcript AI | Powered by Gemma 4",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 9999px;
        background-color: #E0E7FF;
        color: #3730A3;
        margin-right: 0.5rem;
    }
    .info-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_transcriber(model_size: str = "tiny") -> AudioTranscriber:
    """Cache transcription model instance to prevent reloading on every rerun."""
    return AudioTranscriber(model_size=model_size, device="cpu", compute_type="int8")


# Session state initialization
if "transcript_result" not in st.session_state:
    st.session_state.transcript_result = None
if "learning_notes" not in st.session_state:
    st.session_state.learning_notes = None
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "sample_loaded" not in st.session_state:
    st.session_state.sample_loaded = False


# Sidebar Configuration
with st.sidebar:
    st.markdown("### ⚙️ Settings & Configuration")

    api_key_env = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=api_key_env if api_key_env else "",
        type="password",
        help="Free key from aistudio.google.com for Gemma 4 access.",
    )
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    model_id = st.selectbox(
        "Gemma Model Variant",
        options=[
            "gemma-4-26b-a4b-it",
            "gemma-3-27b-it",
            "gemma-3-12b-it",
            "gemma-3-4b-it",
            "gemma-2-27b-it",
            "gemma-2-9b-it",
        ],
        index=0,
        help="Targeting the 'Best Use of Gemma 4' challenge track.",
    )

    whisper_size = st.selectbox(
        "Whisper Model Size",
        options=["tiny", "base", "small"],
        index=0,
        help="Tiny runs ultra-fast locally on CPU for rapid hackathon testing.",
    )

    st.markdown("---")
    st.markdown("### 🏆 Hackathon Tracks")
    st.markdown('<span class="badge">Best Use of Gemma 4</span>', unsafe_allow_html=True)
    st.markdown('<span class="badge">Best Open-Source AI</span>', unsafe_allow_html=True)
    st.markdown(
        "<small>Built for **Otaku.dev '26 — Hacktoberfest Hack Day Chennai**</small>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🔒 Privacy Notice")
    st.caption(
        "Audio transcription runs entirely on your local machine using Faster-Whisper. "
        "Only extracted text is transmitted to the Gemini API for Gemma 4 summarization."
    )


# Main Interface Header
st.markdown('<div class="main-title">🎙️ Live Transcript AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Turn spoken content into searchable transcripts, intelligent notes, and interactive learning.</div>',
    unsafe_allow_html=True,
)

# Step 1: Upload or Sample selection
st.markdown("### 1. Audio / Video Input")
col_upload, col_sample = st.columns([3, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "Upload lecture, talk, or meeting recording (MP3, WAV, M4A, MP4, WebM)",
        type=["mp3", "wav", "m4a", "mp4", "webm", "ogg"],
        help="Maximum file size 100MB",
    )

with col_sample:
    st.write("Or try demo audio:")
    if st.button("Load Hackathon Sample", help="Loads pre-recorded test speech"):
        sample_path = os.path.join("samples", "sample_speech.wav")
        if os.path.exists(sample_path):
            st.session_state.sample_path = sample_path
            st.session_state.sample_loaded = True
            st.success("Sample speech loaded!")
        else:
            st.error("Sample audio file not found.")

audio_to_process = None

if uploaded_file is not None:
    # Save uploaded file safely to temp file
    temp_dir = tempfile.gettempdir()
    suffix = os.path.splitext(uploaded_file.name)[1]
    temp_file_path = os.path.join(temp_dir, f"uploaded_audio_{uploaded_file.name}")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.read())
    audio_to_process = temp_file_path
    st.audio(uploaded_file)
elif st.session_state.get("sample_loaded", False):
    audio_to_process = st.session_state.sample_path
    st.audio(audio_to_process)


# Step 2: Transcription Action
if audio_to_process:
    if st.button("🚀 Transcribe Audio", type="primary"):
        with st.spinner("Transcribing audio locally with Faster-Whisper..."):
            try:
                transcriber = get_transcriber(model_size=whisper_size)
                result = transcriber.transcribe(audio_to_process)
                st.session_state.transcript_result = result
                # Automatically reset old notes when new audio is processed
                st.session_state.learning_notes = None
                st.session_state.qa_history = []
                st.success(f"✓ Transcribed in {result.duration}s (Language: {result.detected_language.upper()})")
            except Exception as e:
                st.error(f"Transcription error: {str(e)}")


# Step 3: Display Results if Available
if st.session_state.transcript_result:
    res: TranscriptionResult = st.session_state.transcript_result

    tab_transcript, tab_notes, tab_qa, tab_export = st.tabs(
        ["📜 Transcript", "💡 AI Learning Notes", "❓ Ask the Transcript", "💾 Export"]
    )

    # TAB 1: Transcript View
    with tab_transcript:
        col_view, col_stats = st.columns([3, 1])
        with col_stats:
            st.metric("Detected Language", res.detected_language.upper())
            st.metric("Processing Time", f"{res.duration}s")
            st.metric("Segments Count", len(res.segments))

        with col_view:
            show_timestamps = st.checkbox("Show Timestamps", value=True)
            if show_timestamps:
                st.text_area(
                    "Timestamped Transcript",
                    value=res.format_timestamped(),
                    height=300,
                )
            else:
                st.text_area(
                    "Plain Text Transcript",
                    value=res.full_text,
                    height=300,
                )

    # TAB 2: AI Learning Notes (Gemma 4)
    with tab_notes:
        if st.session_state.learning_notes:
            st.markdown(st.session_state.learning_notes)
            if st.button("🔄 Regenerate Notes with Gemma 4"):
                st.session_state.learning_notes = None
                st.rerun()
        else:
            st.info("Generate structured summaries and key concepts using Google Gemma 4.")
            if st.button("✨ Generate Learning Notes with Gemma 4", type="primary"):
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    st.warning("Please configure your Gemini API Key in the left sidebar to use Gemma 4.")
                else:
                    with st.spinner(f"Analyzing transcript with {model_id}..."):
                        try:
                            g_client = GemmaClient(api_key=api_key, model_id=model_id)
                            generator = NotesGenerator(gemma_client=g_client)
                            notes = generator.generate_learning_notes(res.full_text)
                            st.session_state.learning_notes = notes
                            st.rerun()
                        except Exception as e:
                            st.error(f"Gemma 4 generation error: {str(e)}")

    # TAB 3: Grounded Q&A
    with tab_qa:
        st.markdown("### Ask any question about the transcript")
        st.caption("Answers are strictly grounded in what the speaker stated.")

        question = st.text_input("Enter your question:", placeholder="What did the speaker say about...?")
        if st.button("🔍 Get Grounded Answer"):
            if not question:
                st.warning("Please enter a question.")
            else:
                api_key = os.getenv("GEMINI_API_KEY")
                if not api_key:
                    st.warning("Please configure your Gemini API Key in the sidebar.")
                else:
                    with st.spinner("Searching transcript and formulating answer..."):
                        try:
                            g_client = GemmaClient(api_key=api_key, model_id=model_id)
                            qa_engine = QAEngine(gemma_client=g_client)
                            qa_response = qa_engine.answer_question(
                                question=question,
                                transcript_text=res.full_text,
                                segments=res.segments,
                            )
                            # Record history
                            st.session_state.qa_history.insert(0, {
                                "question": question,
                                "answer": qa_response["answer"],
                                "grounded": qa_response["grounded"],
                                "sources": qa_response["sources"],
                            })
                        except Exception as e:
                            st.error(f"Error answering question: {str(e)}")

        # Render Q&A History
        for item in st.session_state.qa_history:
            st.markdown(f"**Q: {item['question']}**")
            st.markdown(f"**A:** {item['answer']}")
            if item.get("sources"):
                with st.expander("📍 Supporting Evidence Passages"):
                    for src in item["sources"]:
                        start_m, start_s = divmod(int(src["start"]), 60)
                        st.caption(f"[{start_m:02d}:{start_s:02d}] *\"{src['text']}\"*")
            st.markdown("---")

    # TAB 4: Export Options
    with tab_export:
        st.markdown("### Download Transcripts and Study Materials")
        col_txt, col_md, col_json = st.columns(3)

        txt_data = ExportManager.export_as_txt(res.full_text, res.format_timestamped())
        col_txt.download_button(
            label="📥 Download Transcript (.TXT)",
            data=txt_data,
            file_name="transcript.txt",
            mime="text/plain",
        )

        if st.session_state.learning_notes:
            md_data = ExportManager.export_as_markdown(
                title="Learning Notes & Concepts",
                notes_markdown=st.session_state.learning_notes,
                transcript_text=res.full_text,
                metadata={"Language": res.detected_language, "Model": model_id},
            )
            col_md.download_button(
                label="📥 Download Study Notes (.MD)",
                data=md_data,
                file_name="learning_notes.md",
                mime="text/markdown",
            )
        else:
            col_md.info("Generate notes to enable Markdown export.")

        json_data = ExportManager.export_as_json(
            transcript_result=res.to_dict(),
            learning_notes=st.session_state.learning_notes or "",
            qa_history=st.session_state.qa_history,
        )
        col_json.download_button(
            label="📥 Download Full Session (.JSON)",
            data=json_data,
            file_name="session_data.json",
            mime="application/json",
        )
