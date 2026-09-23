from g4f.client import Client
import google.generativeai as genai
import streamlit as st

# הגדרות עמוד ותמיכה מלאה בעברית (RTL)
st.set_page_config(
    page_title="🌐 Universal Polymath AI Hub", page_icon="🎓", layout="wide"
)

st.markdown(
    """
<style>
    .stChatMessage { direction: rtl; text-align: right; }
    div[data-testid="stMarkdownContainer"] p { direction: rtl; text-align: right; }
    h1, h2, h3, h4 { direction: rtl; text-align: right; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🎓 Universal Polymath AI Hub (24/7)")
st.caption(
    "פלטפורמת בינה אקדמית אינטגרטיבית. שולטת ומחברת בין כל מקצועות הלימוד:"
    " מדעי הרוח, חברה, משפטים, כלכלה, רפואה, מדעים מדויקים והנדסה."
)

# סרגל צד – הגדרות ניתוח ורשת ה-AI
with st.sidebar:
  st.header("⚙️ הגדרות אינטגרציה")

  synthesis_mode = st.radio(
      "אופי הניתוח והחשיבה:",
      [
          (
              "🌐 אינטגרטיבי ורב-תחומי (ערבוב והצלבת תחומים שונים)"
          ),  # ברירת המחדל
          "🎯 עומק ממוקד (התמקדות מעמיקה בדיסציפלינה אחת)",
      ],
      index=0,
  )

  provider_mode = st.radio(
      "מנוע חיבור:",
      [
          "ללא מפתח (חינם דרך GitHub / g4f)",
          "מפתח רשמי חינמי (Google Gemini API)",
      ],
  )

  gemini_api_key = ""
  selected_model = "gpt-4o"

  if provider_mode == "מפתח רשמי חינמי (Google Gemini API)":
    gemini_api_key = st.text_input(
        "מפתח Gemini (מ-aistudio.google.com):",
        type="password",
        value=st.secrets.get("GEMINI_API_KEY", ""),
    )
  else:
    selected_model = st.selectbox(
        "בחר מודל AI:",
        ["gpt-4o", "claude-3.5-sonnet", "gemini-1.5-flash", "llama-3.3-70b"],
        index=0,
    )

  if st.button("🧹 נקה שיחה"):
    st.session_state.messages = []
    st.rerun()

# אתחול היסטוריה
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "שלום! אני מוכן לניתוח ולמידה בכל תחום דעת ומקצוע אקדמי —"
          " מפילוסופיה, משפטים, כלכלה ופסיכולוגיה ועד ביולוגיה, מתמטיקה,"
          " פיזיקה והנדסה. שאל כל שאלה, בקש הצלבה בין עולמות שונים או פתרון"
          " בעיות מורכבות."
      ),
  }]

# הצגת השיחה
for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.markdown(msg["content"])

# הנחיית העל לפולימאת (System Prompt מותאם לשזירת תחומים)
if synthesis_mode == "🌐 אינטגרטיבי ורב-תחומי (ערבוב והצלבת תחומים שונים)":
  system_instruction = """אתה איש אשכולות (Polymath) ומומחה אקדמי אוניברסלי ברמה הגבוהה ביותר.
תפקידך לשלוט ולשלב בין כל תחומי הדעת והמקצועות:
- מדעי הרוח: פילוסופיה, אתיקה, היסטוריה, בלשנות וספרות.
- מדעי החברה וההתנהגות: פסיכולוגיה, קוגניציה, כלכלה, סוציולוגיה, מדע המדינה ואנתרופולוגיה.
- מקצועות יישומיים: משפטים, מנהל עסקים, אסטרטגיה, שיווק ופיננסים.
- בריאות ורפואה: פיזיולוגיה, תזונה, ביוכימיה, אנטומיה, אימונולוגיה ופתולוגיה.
- מדעים מדויקים והנדסה: מתמטיקה, פיזיקה, כימיה, מדעי המחשב ומערכות מורכבות.

דגש קריטי: בצע הצלבה, אנלוגיות וסינתזה סיבתית בין דיסציפלינות שונות ('ערבוב' מושגי). 
הראה כיצד עקרונות מתחום אחד מאירים תופעות בתחום אחר (למשל: תרמודינמיקה בכלכלה, תורת המשחקים באבולוציה ופסיכולוגיה, או ביו-אתיקה במשפט וטכנולוגיה). 
ענה בעברית עשירה, אקדמית, מדויקת ומובנית."""
else:
  system_instruction = """אתה מומחה אקדמי מעמיק בכל תחום דעת ומקצוע. 
נתח את השאלה מתוך עקרונות היסוד של הדיסציפלינה הרלוונטית, בצורה שיטתית, מנומקת, מדויקת ואנליטית בעברית גבוהה."""

# קליטת קלט
if prompt := st.chat_input("שאל שאלה, בקש ניתוח קורס או הצלבה בין תחומים..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("מצליב עקרונות ובונה ניתוח אינטגרטיבי..."):
      response_text = ""

      # שימוש במפתח Gemini
      if (
          provider_mode == "מפתח רשמי חינמי (Google Gemini API)"
          and gemini_api_key
      ):
        try:
          genai.configure(api_key=gemini_api_key)
          model = genai.GenerativeModel("gemini-1.5-flash")
          full_prompt = (
              f"{system_instruction}\n\nבקשת המשתמש:\n{prompt}\n\nתשובה"
              " אינטגרטיבית:"
          )
          res = model.generate_content(full_prompt)
          response_text = res.text
        except Exception as e:
          response_text = f"שגיאה בהתחברות ל-API: {e}"

      # שימוש בחינם דרך g4f ללא מפתחות
      else:
        try:
          client = Client()
          formatted_messages = [
              {"role": "system", "content": system_instruction}
          ]
          for m in st.session_state.messages[:-1]:
            formatted_messages.append(
                {"role": m["role"], "content": m["content"]}
            )
          formatted_messages.append({"role": "user", "content": prompt})

          resp = client.chat.completions.create(
              model=selected_model, messages=formatted_messages
          )
          response_text = resp.choices[0].message.content
        except Exception as e:
          response_text = f"עומס רגעי בספק ({e}). נסה שוב בעוד כמה שניות או החלף מודל בסרגל הצד."

      st.markdown(response_text)
      st.session_state.messages.append(
          {"role": "assistant", "content": response_text}
      )
