import streamlit as st
from PIL import Image
import io
import json
import re

st.set_page_config(page_title="E-Waste Classifier", page_icon="♻️", layout="wide")

st.markdown("""
<style>
.block-container{max-width:1100px;padding-top:2rem}
.hero{padding:1.5rem 1.7rem;border:1px solid #e5e9ef;border-radius:20px;background:linear-gradient(120deg,#effaf4,#f0f6ff)}
.hero h1{margin:0;color:#18352a;font-size:2.25rem}
.hero p{margin:.45rem 0 0;color:#536b60}
.tip{padding:12px 15px;border-radius:12px;background:#f5f7fa;border:1px solid #e5e9ef}
</style>
""", unsafe_allow_html=True)

CATEGORIES = [
    "Battery", "Mobile phone / tablet", "Computer / laptop",
    "Cable / wire", "Circuit board / electronic component",
    "Monitor / television", "Printer / scanner", "Other electronic waste"
]

def classify_with_gemini(image, api_key, model):
    from google import genai
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an electronic-waste sorting assistant. Inspect the uploaded image and classify
the main visible discarded electronic item into exactly one best category from:
{", ".join(CATEGORIES)}.
Do not claim certainty if the image is unclear. Never advise opening, dismantling,
crushing, burning, puncturing or handling damaged batteries.
Return valid JSON only with these keys:
category (must be one of the exact category names above),
confidence (integer 0 to 100),
reason (one or two short sentences describing visible evidence),
safe_next_step (one short safe disposal suggestion),
uncertain (true or false).
If the image is not clearly electronic waste, use "Other electronic waste" and explain.
"""
    response = client.models.generate_content(
        model=model,
        contents=[prompt, image]
    )
    raw = response.text or ""
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        raise ValueError("The AI response could not be read. Please try again.")
    data = json.loads(match.group(0))
    if data.get("category") not in CATEGORIES:
        data["category"] = "Other electronic waste"
    data["confidence"] = max(0, min(100, int(data.get("confidence", 0))))
    return data

def demo_result():
    return {
        "category": "Other electronic waste",
        "confidence": 0,
        "reason": "Demo mode does not analyse image contents. Connect Gemini AI to classify the uploaded item.",
        "safe_next_step": "Keep the item intact and take it to an authorised e-waste collection point.",
        "uncertain": True
    }

with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Gemini API key", type="password", help="Optional for opening the app; required for real image classification.")
    model = st.selectbox("Gemini model", ["gemini-2.5-flash", "gemini-2.0-flash"], index=0)
    if api_key:
        st.success("API key entered for this session.")
    else:
        st.info("Demo mode. Add a Gemini key for actual image analysis.")
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.caption("Privacy: When Gemini is enabled, the uploaded image is sent to Google to generate a classification. Do not upload images containing personal or confidential information.")

st.markdown("""
<div class="hero">
<h1>♻️ E-Waste Classification</h1>
<p>Upload a photo of an electronic item to identify its likely e-waste category and get a safe disposal suggestion.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1])
with left:
    st.subheader("1. Upload an item photo")
    uploaded = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "webp"])
    if uploaded:
        try:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded item", use_container_width=True)
        except Exception:
            st.error("This image could not be opened. Please upload a JPG, PNG or WEBP image.")
            image = None
    else:
        image = None
        st.markdown('<div class="tip">Take a clear photo with one item visible, good lighting and minimal background clutter.</div>', unsafe_allow_html=True)

with right:
    st.subheader("2. Classify the item")
    st.write("The classifier checks the visible item and returns a category, confidence estimate and a safe next step.")
    if st.button("Classify E-Waste", type="primary", use_container_width=True, disabled=image is None):
        if not api_key:
            st.session_state["classification"] = demo_result()
            st.session_state["demo_mode"] = True
        else:
            try:
                with st.spinner("Analysing the image..."):
                    result = classify_with_gemini(image, api_key, model)
                st.session_state["classification"] = result
                st.session_state["demo_mode"] = False
            except Exception as exc:
                st.error(f"Classification failed: {exc}")
                st.caption("Check your internet connection, API key, selected model and Google AI Studio usage limits.")

    result = st.session_state.get("classification")
    if result:
        st.divider()
        st.subheader("3. Classification result")
        if st.session_state.get("demo_mode"):
            st.warning("Demo mode: the image has not actually been analysed. Add a Gemini API key to enable classification.")
        st.markdown(f"### {result['category']}")
        st.metric("AI confidence estimate", f"{result['confidence']}%" if result["confidence"] else "Not available")
        st.write("**Why this category?**")
        st.write(result["reason"])
        st.write("**Safe next step**")
        st.success(result["safe_next_step"])
        if result.get("uncertain"):
            st.warning("The result is uncertain. Confirm the item type with a local authorised e-waste collection service.")

st.divider()
st.subheader("Categories supported")
cols = st.columns(4)
for i, category in enumerate(CATEGORIES):
    cols[i % 4].markdown(f"- {category}")

st.markdown("""
<div class="tip">
<b>Safety reminder:</b> Do not dismantle, burn, crush or puncture electronic waste.
Do not handle swollen, leaking or damaged batteries. Keep such items away from heat
and seek guidance from an authorised e-waste collection or recycling facility.
</div>
""", unsafe_allow_html=True)
st.caption("Student project prototype. AI classifications can be wrong; verify before sorting or disposal. Follow local e-waste regulations.")
