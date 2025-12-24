import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import datetime
import textwrap
import io

# --- APP CONFIGURATION ---
#st.set_page_config(page_title="PLAYER REGISTRATION", page_icon="https://t3.ftcdn.net/jpg/09/26/69/04/360_F_926690484_av0xyDEUluJzf2yLeuzTPV3D1WrA04Gc.jpg", width=100)
PICKLEBALL_IMAGE = "https://t3.ftcdn.net/jpg/09/26/69/04/360_F_926690484_av0xyDEUluJzf2yLeuzTPV3D1WrA04Gc.jpg" 

st.image(PICKLEBALL_IMAGE, width=100)
st.title("SAP-SAP Pickleball Assessment")

st.set_page_config(page_title="PLAYER REGISTRATION", page_icon="https://t3.ftcdn.net/jpg/09/26/69/04/360_F_926690484_av0xyDEUluJzf2yLeuzTPV3D1WrA04Gc.jpg", width=100)
# Developed by AlwinLagnitonBSCS
st.markdown("<h5 style='text-align: center; color: gray;'>Developed by AlwinLagniton, BSCS</h5>", unsafe_allow_html=True)

# --- INITIALIZE SESSION STATE ---
if 'page' not in st.session_state:
    st.session_state.page = 'profile'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# --- QUESTIONS LIST ---
QUESTIONS = [
    "I know where to stand at the beginning of each point",
    "I usually get my serves 'in'",
    "I usually let the return of serve bounce",
    "I am getting the hang of keeping score",
    "I can often keep the ball in play",
    "I know what a dink shot is",
    "I have the basic rules down 100%",
    "I am working on getting my serves and return of serves deeper",
    "I am working on getting my dinks shallower/lower",
    "I am capable of hitting a few dinks in a row",
    "I can usually hit backhand shots when I need to",
    "I am trying to add more power or softness to my game",
    "I know almost all the 'special case' rules",
    "My serves and returns are almost always deep",
    "I sometimes try to hit a 3rd shot drop shot",
    "I try to be strategic of how and where I hit the ball",
    "I have wide variety of shots in my arsenal",
    "I actively work with my partner to win a point",
    "I can often anticipate my opponents shots",
    "I often finish a point when my opponent gives me an opening",
    "I am usually consistent in drop shots and dink shots",
    "I almost always play in the non-volley line",
    "With a good partner, I can cover almost any shot",
    "I try to be patient and wait for the opening",
    "I can consistently convert a hard shot to a soft shot",
    "I am almost always patient and wait for the opening",
    "I rarely make unforced errors",
    "I consistently use power and finesse to my advantage",
    "I can easily sustain a rally of 40 or more shots",
    "I have competed in tournaments at the 4.5 level or higher"
]


# --- HELPER FUNCTIONS: IMAGE GENERATION ---
def generate_rating_card(data, score, rating):
    img = Image.new('RGB', (1000, 750), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    blue_accent = (59, 142, 208)
    draw.rectangle([20, 20, 980, 730], outline=blue_accent, width=15)

    try:
        # Note: On cloud servers, standard fonts like Arial might not exist.
        # For best results, upload your .ttf files to your GitHub repo.
        f_b = "arialbd.ttf";
        f_r = "arial.ttf"
        font_small = ImageFont.truetype(f_r, 20)
        font_name = ImageFont.truetype(f_b, 35)
        font_res = ImageFont.truetype(f_b, 100)
        font_score = ImageFont.truetype(f_r, 40)
    except:
        font_small = font_name = font_res = font_score = ImageFont.load_default()

    if data['photo']:
        profile = Image.open(data['photo']).convert("RGB").resize((260, 260))
        img.paste(profile, (70, 70))
        draw.rectangle([70, 70, 330, 330], outline=(200, 200, 200), width=3)

    draw.text((360, 80), "OFFICIAL SKILL RATING CERTIFICATE", font=font_small, fill=(130, 130, 130))
    draw.text((360, 120), data['name'].upper(), font=font_name, fill=(0, 0, 0))
    draw.text((360, 195), f"Agency: {data['agency']}", font=font_small, fill=(60, 60, 60))
    draw.text((360, 230), f"AGE/GENDER: {data['age']} / {data['gender']}", font=font_small, fill=(0, 0, 0))

    draw.line((100, 400, 900, 400), fill=(230, 230, 230), width=3)
    draw.text((500, 540), rating.upper(), font=font_res, fill=blue_accent, anchor="mm")
    draw.text((500, 660), f"SCORE: {score:.3f}", font=font_score, fill=(0, 0, 0), anchor="mm")

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    draw.text((500, 700), f"Issued: {ts} | SAPSAP System", font=font_small, fill=(180, 180, 180), anchor="mm")

    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def generate_transcript(data, answers):
    img = Image.new('RGB', (1000, 2400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((50, 50), f"TRANSCRIPT: {data['name'].upper()}", fill=(0, 0, 0))

    y = 120
    for i, q in enumerate(QUESTIONS):
        ans = answers.get(i, "N/A")
        lines = textwrap.wrap(f"{i + 1}. {q}", width=80)
        for line in lines:
            draw.text((50, y), line, fill=(60, 60, 60))
            y += 35
        draw.text((850, y - 35), f"[{ans}]", fill=(34, 139, 34) if ans == "Yes" else (178, 34, 34))
        y += 40

    final_img = img.crop((0, 0, 1000, y + 50))
    buf = io.BytesIO()
    final_img.save(buf, format="JPEG")
    return buf.getvalue()


# --- PAGE 1: PLAYER PROFILE ---
if st.session_state.page == 'profile':
    st.title("🏓 Player Registration")
    with st.form("profile_form"):
        name = st.text_input("Full Name")
        age = st.text_input("Age")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        agency = st.text_input("Agency")
        photo = st.file_uploader("Upload Profile Picture (.jpg)", type=["jpg", "jpeg"])

        submit = st.form_submit_button("GO TO INSTRUCTIONS")
        if submit:
            if name and photo:
                st.session_state.user_data = {"name": name, "age": age, "gender": gender, "agency": agency,
                                              "photo": photo}
                st.session_state.page = 'instructions'
                st.rerun()
            else:
                st.error("Please provide your Name and Photo.")

# --- PAGE 2: INSTRUCTIONS ---
elif st.session_state.page == 'instructions':
    st.title("📖 Instructions")
    st.info("""
    • Answer the questions conscientiously.
    • Check 'Yes' for skills you have mastered.
    • Check 'No' if you are still developing or unsure.
    • You must answer every question.
    • At the end, you can download your Certificate and Transcript.
    """)
    st.caption("🔒 Privacy Note: Your data and photo are processed in real-time and are NOT stored on our servers. Once you close this tab, all information is deleted.")
    if st.button("START ASSESSMENT"):
        st.session_state.page = 'test'
        st.rerun()

# --- PAGE 3: ASSESSMENT ---
elif st.session_state.page == 'test':
    st.title("📝 Skill Assessment")
    responses = {}
    for i, q in enumerate(QUESTIONS):
        responses[i] = st.radio(f"{i + 1}. {q}", ["No", "Yes"], index=None, key=f"q{i}")
        st.divider()

    if st.button("PROCESS RESULT"):
        if None in responses.values():
            st.warning("Please answer all questions before proceeding.")
        else:
            st.session_state.answers = responses
            st.session_state.page = 'result'
            st.rerun()

# --- PAGE 4: RESULT ---
elif st.session_state.page == 'result':
    st.title("🏆 Your Rating")

    yes_count = sum(1 for v in st.session_state.answers.values() if v == "Yes")
    score = yes_count * 0.1667

    if score < 2.0:
        rating = "Newbie"
    elif 2.1 <= score < 2.6:
        rating = "Beginner"
    elif 2.6 <= score < 3.1:
        rating = "Novice"
    elif 3.1 <= score < 3.6:
        rating = "Intermediate"
    elif 3.6 <= score < 4.1:
        rating = "Advance"
    else:
        rating = "Expert"

    st.balloons()

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(st.session_state.user_data['photo'], caption=st.session_state.user_data['name'], width=200)
    with col2:
        st.header(f"Rating: {rating.upper()}")
        st.subheader(f"Score: {score:.4f}")

    st.divider()

    # Generate Files
    cert_bytes = generate_rating_card(st.session_state.user_data, score, rating)
    trans_bytes = generate_transcript(st.session_state.user_data, st.session_state.answers)

    st.download_button("📩 Download Rating Certificate", data=cert_bytes, file_name="Certificate.jpg", mime="image/jpeg")
    st.download_button("📄 Download Transcript", data=trans_bytes, file_name="Transcript.jpg", mime="image/jpeg")

    if st.button("RETAKE TEST"):
        st.session_state.page = 'profile'

        st.rerun()





