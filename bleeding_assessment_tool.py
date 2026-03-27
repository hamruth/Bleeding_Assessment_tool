import streamlit as st
import datetime
import io
import base64
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── reportlab imports ─────────────────────────────────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, KeepTogether)
from reportlab.platypus import Flowable

st.set_page_config(
    page_title="Bleeding Assessment Tool · ISTH BAT",
    page_icon="🩸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# TRANSLATIONS
# ══════════════════════════════════════════════════════════════════════════════
T = {
    "English": {
        "lang_label":"🌐 Language","app_title":"Bleeding Assessment Tool",
        "app_sub":"A structured clinical screening instrument based on the ISTH BAT framework.",
        "pill_q":"Questions","pill_min":"Minutes","pill_result":"Instant Results","pill_isth":"ISTH BAT Based",
        "purpose_title":"Purpose","purpose_body":"Screen for hemostatic defects and determine pre-test probability",
        "instr_title":"Instructions","instr_body":"Answer Yes or No based on your personal bleeding history",
        "score_title":"Scoring","score_body":"Weighted scoring — severe symptoms carry higher points",
        "outcome_title":"Outcome","outcome_body":"Risk classification with clinical guidance for next steps",
        "patient_heading":"Patient Information","patient_sub":"Please fill in your details before starting",
        "pt_name":"Full Name","pt_age":"Age (years)","pt_date":"Date of Assessment",
        "pt_gender_label":"Gender","pt_id":"Patient ID / Reference (optional)",
        "pt_name_ph":"Enter patient name","pt_id_ph":"e.g. OPD-2024-001",
        "name_required":"⚠️ Please enter patient name to continue.",
        "age_required":"⚠️ Please enter a valid age (1–120).",
        "gender_heading":"Select Your Gender","gender_sub":"Questions will be personalised based on your selection",
        "male":"♂  Male","female":"♀  Female","other":"⚧  Other / Prefer not to say",
        "begin":"🩸  Begin Assessment","isth_label":"ISTH Bleeding Assessment",
        "yes":"✅  Yes","yes_sel":"✅  Yes  ✓","no":"❌  No","no_sel":"❌  No  ✓",
        "back":"← Back","skip":"Skip →",
        "results_title":"Assessment Results","results_sub":"ISTH Bleeding Assessment Tool · Clinical Screening",
        "positive":"Positive","negative":"Negative","answered":"Answered","weighted":"Weighted Score",
        "pos_domains":"🔴 Positive Symptom Domains",
        "no_positive":"✅ No positive bleeding symptoms reported across all domains.",
        "summary":"📝 Complete Answer Summary","chart_title":"Score Visualisation",
        "download_pdf":"📄  Download PDF Report","pdf_generating":"Generating PDF...",
        "disclaimer":"⚠️ Medical Disclaimer: This tool is for educational and screening purposes only. "
                     "It does not constitute a medical diagnosis. Please consult a qualified haematologist "
                     "or physician for clinical evaluation based on ISTH BAT guidelines.",
        "retake":"🔄  Retake Assessment","review":"← Review Questions",
        "of":"/","question":"Question","gender_badge":"Gender",
        "risk_low":"Low Risk","risk_mild":"Borderline / Mild","risk_mod":"Moderate Risk","risk_high":"High Risk — Urgent",
        "adv_low":"Responses suggest low likelihood of a significant bleeding disorder. Routine follow-up recommended.",
        "adv_mild":"Some bleeding symptoms present. Clinical evaluation and basic haematology workup (CBC, PT, aPTT) advisable.",
        "adv_mod":"Multiple bleeding symptoms present. Referral to haematologist recommended for VWF assays and platelet function tests.",
        "adv_high":"Significant bleeding symptoms across multiple domains. Urgent haematology referral strongly advised. Comprehensive workup including factor assays and platelet aggregation studies required.",
        "pdf_title":"ISTH Bleeding Assessment Report","pdf_patient":"Patient Details",
        "pdf_name":"Name","pdf_age":"Age","pdf_date":"Date","pdf_gender":"Gender","pdf_id":"Reference ID",
        "pdf_score":"Score Summary","pdf_risk":"Risk Classification","pdf_advice":"Clinical Recommendation",
        "pdf_domains":"Positive Symptom Domains","pdf_answers":"Detailed Answer Summary",
        "pdf_footer":"This report is for screening purposes only and does not constitute a medical diagnosis.",
        "pdf_yes":"YES","pdf_no":"NO","pdf_na":"—",
        "proceed":"→  Enter Patient Details",
        "next_gender":"→  Select Gender",
    },
    "Malayalam": {
        "lang_label":"🌐 ഭാഷ","app_title":"രക്തസ്രാവ വിലയിരുത്തൽ ഉപകരണം",
        "app_sub":"ISTH BAT ചട്ടക്കൂടിനെ അടിസ്ഥാനമാക്കിയ ക്ലിനിക്കൽ സ്ക്രീനിംഗ് ഉപകരണം.",
        "pill_q":"ചോദ്യങ്ങൾ","pill_min":"മിനിറ്റ്","pill_result":"തൽക്ഷണ ഫലം","pill_isth":"ISTH BAT",
        "purpose_title":"ലക്ഷ്യം","purpose_body":"ഹീമോസ്റ്റാറ്റിക് തകരാറുകൾ കണ്ടെത്തുക",
        "instr_title":"നിർദ്ദേശങ്ങൾ","instr_body":"അതെ അല്ലെങ്കിൽ ഇല്ല എന്ന് ഉത്തരം നൽകുക",
        "score_title":"സ്കോറിംഗ്","score_body":"ഭാരം നൽകിയ സ്കോറിംഗ്",
        "outcome_title":"ഫലം","outcome_body":"അപകടസാധ്യത വർഗ്ഗീകരണം",
        "patient_heading":"രോഗി വിവരങ്ങൾ","patient_sub":"ആരംഭിക്കുന്നതിന് മുമ്പ് വിശദാംശങ്ങൾ നൽകുക",
        "pt_name":"പൂർണ്ണ നാമം","pt_age":"പ്രായം (വർഷം)","pt_date":"വിലയിരുത്തൽ തീയതി",
        "pt_gender_label":"ലിംഗം","pt_id":"രോഗി ID (ഓപ്ഷണൽ)",
        "pt_name_ph":"രോഗിയുടെ പേര്","pt_id_ph":"ഉദാ: OPD-2024-001",
        "name_required":"⚠️ തുടരാൻ രോഗിയുടെ പേര് നൽകുക.",
        "age_required":"⚠️ സാധുവായ പ്രായം നൽകുക (1–120).",
        "gender_heading":"ലിംഗം തിരഞ്ഞെടുക്കുക","gender_sub":"തിരഞ്ഞെടുപ്പ് അനുസരിച്ച് ചോദ്യങ്ങൾ ക്രമീകരിക്കും",
        "male":"♂  പുരുഷൻ","female":"♀  സ്ത്രീ","other":"⚧  മറ്റുള്ളവർ",
        "begin":"🩸  വിലയിരുത്തൽ ആരംഭിക്കുക","isth_label":"ISTH രക്തസ്രാവ വിലയിരുത്തൽ",
        "yes":"✅  അതെ","yes_sel":"✅  അതെ  ✓","no":"❌  ഇല്ല","no_sel":"❌  ഇല്ല  ✓",
        "back":"← തിരിച്ച്","skip":"ഒഴിവാക്കുക →",
        "results_title":"വിലയിരുത്തൽ ഫലങ്ങൾ","results_sub":"ISTH BAT · ക്ലിനിക്കൽ സ്ക്രീനിംഗ്",
        "positive":"പോസിറ്റീവ്","negative":"നെഗറ്റീവ്","answered":"ഉത്തരം","weighted":"ഭാര സ്കോർ",
        "pos_domains":"🔴 പോസിറ്റീവ് ലക്ഷണ മേഖലകൾ",
        "no_positive":"✅ പോസിറ്റീവ് ലക്ഷണങ്ങൾ ഒന്നും ഇല്ല.",
        "summary":"📝 പൂർണ്ണ ഉത്തര സംഗ്രഹം","chart_title":"സ്കോർ ദൃശ്യവൽക്കരണം",
        "download_pdf":"📄  PDF റിപ്പോർട്ട് ഡൗൺലോഡ്","pdf_generating":"PDF തയ്യാറാക്കുന്നു...",
        "disclaimer":"⚠️ ഈ ഉപകരണം സ്ക്രീനിംഗ് ആവശ്യങ്ങൾക്ക് മാത്രം. ഒരു ഡോക്ടറുമായി ആലോചിക്കുക.",
        "retake":"🔄  വീണ്ടും ശ്രമിക്കുക","review":"← ചോദ്യങ്ങൾ അവലോകനം",
        "of":"/","question":"ചോദ്യം","gender_badge":"ലിംഗം",
        "risk_low":"കുറഞ്ഞ അപകടസാധ്യത","risk_mild":"അതിർത്തി / നേരിയ","risk_mod":"മിതമായ അപകടസാധ്യത","risk_high":"ഉയർന്ന — അടിയന്തിരം",
        "adv_low":"ഗുരുതരമായ രക്തസ്രാവ രോഗത്തിന്റെ സാധ്യത കുറവ്. ഡോക്ടറുമായി പതിവ് ഫോളോ-അപ്പ് ശുപാർശ.",
        "adv_mild":"ചില ലക്ഷണങ്ങൾ ഉണ്ട്. CBC, PT, aPTT ഉൾക്കൊള്ളുന്ന ക്ലിനിക്കൽ മൂല്യനിർണ്ണയം ഉചിതം.",
        "adv_mod":"ഒന്നിലധികം ലക്ഷണങ്ങൾ. VWF, പ്ലേറ്റ്ലറ്റ് പ്രവർത്തനം പരിശോധിക്കാൻ ഹീമറ്റോളജിസ്റ്റ് റഫറൽ.",
        "adv_high":"ഒന്നിലധികം മേഖലകളിൽ ഗുരുതരമായ ലക്ഷണങ്ങൾ. ഫാക്ടർ അസ്സേ ഉൾക്കൊള്ളുന്ന അടിയന്തിര ഹീമറ്റോളജി റഫറൽ.",
        "pdf_title":"ISTH രക്തസ്രാവ മൂല്യനിർണ്ണയ റിപ്പോർട്ട്",
        "pdf_patient":"രോഗി വിശദാംശങ്ങൾ","pdf_name":"പേര്","pdf_age":"പ്രായം",
        "pdf_date":"തീയതി","pdf_gender":"ലിംഗം","pdf_id":"റഫറൻസ് ID",
        "pdf_score":"സ്കോർ സംഗ്രഹം","pdf_risk":"അപകടസാധ്യത വർഗ്ഗീകരണം",
        "pdf_advice":"ക്ലിനിക്കൽ ശുപാർശ","pdf_domains":"പോസിറ്റീവ് ലക്ഷണ മേഖലകൾ",
        "pdf_answers":"വിശദ ഉത്തര സംഗ്രഹം",
        "pdf_footer":"ഈ റിപ്പോർട്ട് സ്ക്രീനിംഗ് ആവശ്യങ്ങൾക്ക് മാത്രം. ഇത് ഒരു മെഡിക്കൽ രോഗനിർണ്ണയം അല്ല.",
        "pdf_yes":"അതെ","pdf_no":"ഇല്ല","pdf_na":"—",
        "proceed":"→  രോഗി വിശദാംശങ്ങൾ നൽകുക","next_gender":"→  ലിംഗം തിരഞ്ഞെടുക്കുക",
    },
    "Hindi": {
        "lang_label":"🌐 भाषा","app_title":"रक्तस्राव मूल्यांकन उपकरण",
        "app_sub":"ISTH BAT ढांचे पर आधारित संरचित नैदानिक स्क्रीनिंग उपकरण।",
        "pill_q":"प्रश्न","pill_min":"मिनट","pill_result":"त्वरित परिणाम","pill_isth":"ISTH BAT",
        "purpose_title":"उद्देश्य","purpose_body":"रक्तस्राव दोषों की जांच",
        "instr_title":"निर्देश","instr_body":"हाँ या नहीं में उत्तर दें",
        "score_title":"स्कोरिंग","score_body":"भारित स्कोरिंग",
        "outcome_title":"परिणाम","outcome_body":"जोखिम वर्गीकरण",
        "patient_heading":"रोगी जानकारी","patient_sub":"शुरू करने से पहले विवरण भरें",
        "pt_name":"पूरा नाम","pt_age":"आयु (वर्ष)","pt_date":"मूल्यांकन तिथि",
        "pt_gender_label":"लिंग","pt_id":"रोगी ID (वैकल्पिक)",
        "pt_name_ph":"रोगी का नाम दर्ज करें","pt_id_ph":"जैसे OPD-2024-001",
        "name_required":"⚠️ जारी रखने के लिए रोगी का नाम दर्ज करें।",
        "age_required":"⚠️ वैध आयु दर्ज करें (1–120)।",
        "gender_heading":"अपना लिंग चुनें","gender_sub":"आपके चयन के आधार पर प्रश्न अनुकूलित होंगे",
        "male":"♂  पुरुष","female":"♀  महिला","other":"⚧  अन्य",
        "begin":"🩸  मूल्यांकन शुरू करें","isth_label":"ISTH रक्तस्राव मूल्यांकन",
        "yes":"✅  हाँ","yes_sel":"✅  हाँ  ✓","no":"❌  नहीं","no_sel":"❌  नहीं  ✓",
        "back":"← वापस","skip":"छोड़ें →",
        "results_title":"मूल्यांकन परिणाम","results_sub":"ISTH BAT · नैदानिक स्क्रीनिंग",
        "positive":"सकारात्मक","negative":"नकारात्मक","answered":"उत्तर दिए","weighted":"भारित स्कोर",
        "pos_domains":"🔴 सकारात्मक लक्षण क्षेत्र",
        "no_positive":"✅ सभी क्षेत्रों में कोई सकारात्मक लक्षण नहीं।",
        "summary":"📝 पूर्ण उत्तर सारांश","chart_title":"स्कोर दृश्यावलोकन",
        "download_pdf":"📄  PDF रिपोर्ट डाउनलोड करें","pdf_generating":"PDF बन रही है...",
        "disclaimer":"⚠️ यह उपकरण केवल स्क्रीनिंग के लिए है। यह चिकित्सा निदान नहीं है। कृपया विशेषज्ञ से परामर्श करें।",
        "retake":"🔄  पुनः मूल्यांकन","review":"← प्रश्नों की समीक्षा",
        "of":"/","question":"प्रश्न","gender_badge":"लिंग",
        "risk_low":"कम जोखिम","risk_mild":"सीमा रेखा / हल्का","risk_mod":"मध्यम जोखिम","risk_high":"उच्च जोखिम — अत्यावश्यक",
        "adv_low":"प्रतिक्रियाएं महत्वपूर्ण रक्तस्राव विकार की कम संभावना दर्शाती हैं। नियमित फॉलो-अप की सिफारिश।",
        "adv_mild":"कुछ लक्षण मौजूद हैं। CBC, PT, aPTT सहित नैदानिक मूल्यांकन उचित है।",
        "adv_mod":"कई लक्षण मौजूद हैं। VWF परीक्षण के लिए रक्त रोग विशेषज्ञ को रेफर करें।",
        "adv_high":"कई क्षेत्रों में गंभीर लक्षण। फैक्टर परीक्षण के लिए तत्काल हेमेटोलॉजी रेफरल आवश्यक।",
        "pdf_title":"ISTH रक्तस्राव मूल्यांकन रिपोर्ट",
        "pdf_patient":"रोगी विवरण","pdf_name":"नाम","pdf_age":"आयु","pdf_date":"तिथि",
        "pdf_gender":"लिंग","pdf_id":"संदर्भ ID","pdf_score":"स्कोर सारांश",
        "pdf_risk":"जोखिम वर्गीकरण","pdf_advice":"नैदानिक सिफारिश",
        "pdf_domains":"सकारात्मक लक्षण क्षेत्र","pdf_answers":"विस्तृत उत्तर सारांश",
        "pdf_footer":"यह रिपोर्ट केवल स्क्रीनिंग उद्देश्यों के लिए है और चिकित्सा निदान नहीं है।",
        "pdf_yes":"हाँ","pdf_no":"नहीं","pdf_na":"—",
        "proceed":"→  रोगी जानकारी दर्ज करें","next_gender":"→  लिंग चुनें",
    },
    "Tamil": {
        "lang_label":"🌐 மொழி","app_title":"இரத்தப்போக்கு மதிப்பீட்டு கருவி",
        "app_sub":"ISTH BAT கட்டமைப்பின் அடிப்படையிலான மருத்துவ திரையிடல் கருவி.",
        "pill_q":"கேள்விகள்","pill_min":"நிமிடங்கள்","pill_result":"உடனடி முடிவுகள்","pill_isth":"ISTH BAT",
        "purpose_title":"நோக்கம்","purpose_body":"ஹீமோஸ்டேடிக் குறைபாடுகளை கண்டறிய",
        "instr_title":"வழிமுறைகள்","instr_body":"ஆம் அல்லது இல்லை என பதிலளிக்கவும்",
        "score_title":"மதிப்பெண்","score_body":"எடையிடப்பட்ட மதிப்பெண்",
        "outcome_title":"விளைவு","outcome_body":"ஆபத்து வகைப்பாடு",
        "patient_heading":"நோயாளர் தகவல்","patient_sub":"தொடங்குவதற்கு முன் விவரங்களை நிரப்பவும்",
        "pt_name":"முழு பெயர்","pt_age":"வயது (ஆண்டுகள்)","pt_date":"மதிப்பீட்டு தேதி",
        "pt_gender_label":"பாலினம்","pt_id":"நோயாளர் ID (விருப்பமானால்)",
        "pt_name_ph":"நோயாளரின் பெயரை உள்ளிடவும்","pt_id_ph":"எ.கா. OPD-2024-001",
        "name_required":"⚠️ தொடர நோயாளரின் பெயரை உள்ளிடவும்.",
        "age_required":"⚠️ சரியான வயதை உள்ளிடவும் (1–120).",
        "gender_heading":"உங்கள் பாலினத்தை தேர்ந்தெடுக்கவும்","gender_sub":"உங்கள் தேர்வின் படி கேள்விகள் தனிப்பயனாக்கப்படும்",
        "male":"♂  ஆண்","female":"♀  பெண்","other":"⚧  மற்றவர்கள்",
        "begin":"🩸  மதிப்பீடு தொடங்கவும்","isth_label":"ISTH இரத்தப்போக்கு மதிப்பீடு",
        "yes":"✅  ஆம்","yes_sel":"✅  ஆம்  ✓","no":"❌  இல்லை","no_sel":"❌  இல்லை  ✓",
        "back":"← திரும்பு","skip":"தவிர் →",
        "results_title":"மதிப்பீட்டு முடிவுகள்","results_sub":"ISTH BAT · மருத்துவ திரையிடல்",
        "positive":"நேர்மறை","negative":"எதிர்மறை","answered":"பதிலளித்தது","weighted":"எடையிடப்பட்ட மதிப்பெண்",
        "pos_domains":"🔴 நேர்மறை அறிகுறி பகுதிகள்",
        "no_positive":"✅ எல்லா பகுதிகளிலும் நேர்மறை அறிகுறிகள் எதுவும் இல்லை.",
        "summary":"📝 முழுமையான பதில் சுருக்கம்","chart_title":"மதிப்பெண் காட்சிப்படுத்தல்",
        "download_pdf":"📄  PDF அறிக்கை பதிவிறக்கம்","pdf_generating":"PDF உருவாக்கப்படுகிறது...",
        "disclaimer":"⚠️ இந்த கருவி திரையிடல் நோக்கங்களுக்காக மட்டுமே. தகுதிவாய்ந்த மருத்துவரை அணுகவும்.",
        "retake":"🔄  மீண்டும் மதிப்பீடு","review":"← கேள்விகளை மதிப்பாய்வு",
        "of":"/","question":"கேள்வி","gender_badge":"பாலினம்",
        "risk_low":"குறைந்த ஆபத்து","risk_mild":"எல்லை / லேசான","risk_mod":"மிதமான ஆபத்து","risk_high":"அதிக ஆபத்து — அவசரம்",
        "adv_low":"பதில்கள் குறிப்பிடத்தக்க இரத்தப்போக்கு கோளாறின் குறைந்த சாத்தியத்தை காட்டுகின்றன. வழக்கமான பின்தொடர்தல் பரிந்துரைக்கப்படுகிறது.",
        "adv_mild":"சில அறிகுறிகள் உள்ளன. CBC, PT, aPTT உட்பட மருத்துவ மதிப்பீடு பொருத்தமானது.",
        "adv_mod":"பல அறிகுறிகள் உள்ளன. VWF பரிசோதனைகளுக்கு இரத்தவியல் நிபுணரிடம் அனுப்பவும்.",
        "adv_high":"பல பகுதிகளில் கடுமையான அறிகுறிகள். காரணி பரிசோதனைகளுக்கு அவசர இரத்தவியல் நிபுணர் பரிந்துரை.",
        "pdf_title":"ISTH இரத்தப்போக்கு மதிப்பீட்டு அறிக்கை",
        "pdf_patient":"நோயாளர் விவரங்கள்","pdf_name":"பெயர்","pdf_age":"வயது","pdf_date":"தேதி",
        "pdf_gender":"பாலினம்","pdf_id":"குறிப்பு ID","pdf_score":"மதிப்பெண் சுருக்கம்",
        "pdf_risk":"ஆபத்து வகைப்பாடு","pdf_advice":"மருத்துவ பரிந்துரை",
        "pdf_domains":"நேர்மறை அறிகுறி பகுதிகள்","pdf_answers":"விரிவான பதில் சுருக்கம்",
        "pdf_footer":"இந்த அறிக்கை திரையிடல் நோக்கங்களுக்காக மட்டுமே. இது மருத்துவ நோயறிதல் அல்ல.",
        "pdf_yes":"ஆம்","pdf_no":"இல்லை","pdf_na":"—",
        "proceed":"→  நோயாளர் தகவலை உள்ளிடவும்","next_gender":"→  பாலினத்தை தேர்ந்தெடுக்கவும்",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# QUESTIONS
# ══════════════════════════════════════════════════════════════════════════════
QUESTIONS = {
    "English": [
        {"id":1,"gender":"all","category":"Bruising","weight":1,
         "text":"Do you bruise easily without a clear cause, forming bruises larger than a coin?",
         "hint":"Spontaneous bruising not related to trauma"},
        {"id":2,"gender":"all","category":"Epistaxis","weight":1,
         "text":"Have you ever had nosebleeds lasting more than 10 minutes or requiring medical attention?",
         "hint":"Includes spontaneous and recurrent nosebleeds"},
        {"id":3,"gender":"all","category":"Oral Cavity","weight":1,
         "text":"Do your gums bleed spontaneously or during routine toothbrushing?",
         "hint":"Oral cavity / gum bleeding"},
        {"id":4,"gender":"all","category":"Post-Dental Bleeding","weight":1,
         "text":"Have you ever bled excessively after a tooth extraction or dental procedure?",
         "hint":"Bleeding requiring additional intervention after dental work"},
        {"id":5,"gender":"all","category":"Post-Surgical Bleeding","weight":1,
         "text":"Have you ever had prolonged or heavy bleeding after a surgical procedure?",
         "hint":"Bleeding beyond what was expected post-operatively"},
        {"id":6,"gender":"all","category":"Transfusion","weight":2,
         "text":"Have you ever required a blood transfusion due to a bleeding episode?",
         "hint":"Any transfusion related to bleeding, not surgery itself"},
        {"id":7,"gender":"all","category":"Emergency Bleed","weight":2,
         "text":"Have you ever been hospitalised or visited an emergency department because of bleeding?",
         "hint":"Excludes planned surgical admissions"},
        {"id":8,"gender":"all","category":"Haemarthrosis","weight":2,
         "text":"Have you ever had bleeding into a joint (haemarthrosis) causing pain and swelling?",
         "hint":"Typically knees, elbows, or ankles"},
        {"id":9,"gender":"all","category":"Muscle Haematoma","weight":2,
         "text":"Have you ever had a muscle haematoma (deep bleed inside a muscle)?",
         "hint":"Often occurring without significant trauma"},
        {"id":10,"gender":"all","category":"Haematuria","weight":1,
         "text":"Have you ever noticed blood in your urine without a urinary infection?",
         "hint":"Frank or microscopic haematuria not explained by infection"},
        {"id":11,"gender":"all","category":"GI Bleeding","weight":1,
         "text":"Have you ever had blood in your stools or a confirmed gastrointestinal bleed?",
         "hint":"Melaena, haematochezia, or confirmed GI bleeding"},
        {"id":12,"gender":"all","category":"Family History","weight":1,
         "text":"Has a close family member been diagnosed with a bleeding disorder?",
         "hint":"E.g. haemophilia, von Willebrand disease, platelet disorder"},
        {"id":13,"gender":"all","category":"Wound Bleeding","weight":1,
         "text":"Do minor cuts or wounds take unusually long to stop bleeding (>15 minutes)?",
         "hint":"Bleeding from minor wounds"},
        {"id":14,"gender":"all","category":"Intracranial Bleeding","weight":3,
         "text":"Have you ever had a spontaneous intracranial bleed or bleeding in/around the brain?",
         "hint":"ICH, subdural or subarachnoid haemorrhage not related to trauma"},
        {"id":15,"gender":"all","category":"Petechiae","weight":1,
         "text":"Do you develop small red/purple pin-point spots on the skin (petechiae) without injury?",
         "hint":"Petechiae especially on lower limbs or mucous membranes"},
        {"id":16,"gender":"all","category":"Iron Deficiency","weight":1,
         "text":"Have you been treated for iron-deficiency anaemia due to bleeding?",
         "hint":"Anaemia attributed to chronic blood loss"},
        {"id":17,"gender":"all","category":"Drug-Enhanced Bleeding","weight":1,
         "text":"Do you bleed excessively when taking aspirin, NSAIDs, or blood-thinning medications?",
         "hint":"Disproportionate bleeding on antiplatelet / anticoagulant drugs"},
        {"id":18,"gender":"female","category":"Menorrhagia","weight":1,
         "text":"Do you experience heavy menstrual bleeding (periods lasting >7 days or soaking a pad/tampon every hour)?",
         "hint":"Heavy menstrual bleeding since menarche or worsening over time"},
        {"id":19,"gender":"female","category":"Postpartum Haemorrhage","weight":1,
         "text":"Have you ever had excessive bleeding after childbirth (postpartum haemorrhage >= 500 mL)?",
         "hint":"For patients who have delivered; skip if not applicable"},
        {"id":20,"gender":"female","category":"Pregnancy-Related Bleeding","weight":1,
         "text":"Have you ever had a miscarriage or pregnancy loss associated with heavy bleeding?",
         "hint":"Bleeding requiring medical intervention during or after miscarriage"},
        {"id":18,"gender":"male","category":"Haemophilia Symptoms","weight":2,
         "text":"Have you ever had spontaneous bleeding into muscles or joints without obvious injury?",
         "hint":"Spontaneous deep-tissue bleeding is a hallmark of haemophilia"},
        {"id":19,"gender":"male","category":"Post-Circumcision Bleeding","weight":1,
         "text":"Did you have excessive or prolonged bleeding after circumcision?",
         "hint":"Unusual bleeding following circumcision"},
        {"id":20,"gender":"male","category":"GU Bleeding","weight":1,
         "text":"Have you ever had unexplained blood in your urine on more than one occasion?",
         "hint":"Recurrent haematuria not explained by infection or kidney stones"},
        {"id":18,"gender":"other","category":"Hormonal Bleeding","weight":1,
         "text":"Have you experienced unusual or heavy bleeding related to hormonal changes (if applicable)?",
         "hint":"Skip if not applicable"},
        {"id":19,"gender":"other","category":"Surgical Site Bleeding","weight":1,
         "text":"Have you had prolonged bleeding from any surgical site or procedure?",
         "hint":"Including minor procedures like biopsies"},
        {"id":20,"gender":"other","category":"Recurrent Unexplained Bleeding","weight":1,
         "text":"Have you had recurrent unexplained bleeding from any site requiring medical attention?",
         "hint":"Bleeding episodes without clear cause or trigger"},
    ],
    "Malayalam": [
        {"id":1,"gender":"all","category":"ചതവ്","weight":1,
         "text":"വ്യക്തമായ കാരണമില്ലാതെ നിങ്ങൾക്ക് എളുപ്പത്തിൽ ചതവ് ഉണ്ടാകുന്നുണ്ടോ?",
         "hint":"ആഘാതവുമായി ബന്ധപ്പെടാത്ത സ്വതസ്ഫൂർത്തമായ ചതവ്"},
        {"id":2,"gender":"all","category":"മൂക്കിൽ രക്തം","weight":1,
         "text":"10 മിനിറ്റിൽ കൂടുതൽ നീണ്ടുനിൽക്കുന്ന മൂക്കിൽ നിന്ന് രക്തം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ആവർത്തിക്കുന്ന മൂക്കിൽ നിന്ന് രക്തം ഉൾപ്പെടുന്നു"},
        {"id":3,"gender":"all","category":"വായ്","weight":1,
         "text":"ദന്ത ബ്രഷ് ചെയ്യുമ്പോൾ അല്ലെങ്കിൽ സ്വതസ്ഫൂർത്തമായി മോണ രക്തം ഉണ്ടാകുന്നുണ്ടോ?",
         "hint":"വായ്/മോണ രക്തസ്രാവം"},
        {"id":4,"gender":"all","category":"ദന്ത ചികിത്സ","weight":1,
         "text":"പല്ല് പിഴുതെടുക്കൽ ശേഷം അമിത രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ദന്ത ചികിത്സ ശേഷം അധിക ഇടപെടൽ ആവശ്യമായ രക്തസ്രാവം"},
        {"id":5,"gender":"all","category":"ശസ്ത്രക്രിയ","weight":1,
         "text":"ഒരു ശസ്ത്രക്രിയ ശേഷം ദീർഘനേരം അല്ലെങ്കിൽ അധിക രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ഓപ്പറേഷൻ ശേഷം പ്രതീക്ഷിക്കുന്നതിലും അധികം"},
        {"id":6,"gender":"all","category":"രക്തം മാറ്റൽ","weight":2,
         "text":"ഒരു രക്തസ്രാവ സംഭവം കാരണം നിങ്ങൾക്ക് രക്തം മാറ്റൽ ആവശ്യമായിട്ടുണ്ടോ?",
         "hint":"ശസ്ത്രക്രിയ അല്ലാതെ, രക്തസ്രാവവുമായി ബന്ധപ്പെട്ട ട്രാൻസ്ഫ്യൂഷൻ"},
        {"id":7,"gender":"all","category":"അടിയന്തിര ചികിത്സ","weight":2,
         "text":"രക്തസ്രാവം കാരണം ആശുപത്രിയിൽ പ്രവേശിച്ചിട്ടുണ്ടോ?",
         "hint":"ആസൂത്രിത ശസ്ത്രക്രിയ ഒഴികെ"},
        {"id":8,"gender":"all","category":"സന്ധി രക്തസ്രാവം","weight":2,
         "text":"വേദനയും നീർക്കെട്ടും ഉണ്ടാക്കുന്ന ഒരു സന്ധിക്കകത്ത് രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"സാധാരണ മുട്ട്, കൈമുട്ട് അല്ലെങ്കിൽ കണങ്കൈ"},
        {"id":9,"gender":"all","category":"പേശി ഹിമാറ്റോമ","weight":2,
         "text":"പേശിക്കകത്ത് ആഴത്തിലുള്ള രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"കാര്യമായ ആഘാതം ഇല്ലാതെ"},
        {"id":10,"gender":"all","category":"മൂത്രത്തിൽ രക്തം","weight":1,
         "text":"മൂത്ര അണുബാധ ഇല്ലാതെ മൂത്രത്തിൽ രക്തം ശ്രദ്ധിച്ചിട്ടുണ്ടോ?",
         "hint":"അണുബാധ വഴി വിശദീകരിക്കാനാകാത്ത ഹിമാറ്റൂറിയ"},
        {"id":11,"gender":"all","category":"ദഹന രക്തസ്രാവം","weight":1,
         "text":"മലത്തിൽ രക്തം ഉണ്ടായിട്ടുണ്ടോ?","hint":"സ്ഥിരീകരിച്ച GI രക്തസ്രാവം"},
        {"id":12,"gender":"all","category":"കുടുംബ ചരിത്രം","weight":1,
         "text":"ഒരു അടുത്ത കുടുംബ അംഗത്തിന് ഒരു രക്തസ്രാവ അസുഖം ഉണ്ടെന്ന് കണ്ടെത്തിയിട്ടുണ്ടോ?",
         "hint":"ഹീമോഫിലിയ, VWD, പ്ലേറ്റ്ലറ്റ് അസ്വസ്ഥത"},
        {"id":13,"gender":"all","category":"മുറിവ് രക്തസ്രാവം","weight":1,
         "text":"ചെറിയ മുറിവുകൾ 15 മിനിറ്റിൽ കൂടുതൽ രക്തം ഒഴുകുന്നുണ്ടോ?",
         "hint":"ചെറിയ മുറിവുകളിൽ നിന്ന് അസാധാരണ രക്തസ്രാവം"},
        {"id":14,"gender":"all","category":"തലയ്ക്കകത്ത് രക്തം","weight":3,
         "text":"സ്വതസ്ഫൂർത്തമായ തലച്ചോറിൽ രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ആഘാതവുമായി ബന്ധപ്പെടാത്ത ICH"},
        {"id":15,"gender":"all","category":"ചർമ്മ പൊട്ടൽ","weight":1,
         "text":"ആഘാതം ഇല്ലാതെ ചർമ്മത്തിൽ ചെറിയ ചുവന്ന/ധൂമ്ര ബിന്ദുക്കൾ ഉണ്ടാകുന്നുണ്ടോ?",
         "hint":"പ്രത്യേകിച്ച് കൈകൾ/കാലുകൾ"},
        {"id":16,"gender":"all","category":"അനിമിയ","weight":1,
         "text":"രക്തസ്രാവം കാരണം ഇരുമ്പ് കുറവ് അനിമിയ ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"വിട്ടുമാറാത്ത രക്ത നഷ്ടം കാരണം അനിമിയ"},
        {"id":17,"gender":"all","category":"മരുന്ന് രക്തസ്രാവം","weight":1,
         "text":"ആസ്പിരിൻ, NSAIDs കഴിക്കുമ്പോൾ അമിത രക്തസ്രാവം ഉണ്ടാകുന്നുണ്ടോ?",
         "hint":"ആൻറിപ്ലേറ്റ്ലറ്റ് മരുന്നുകളിൽ അസമാനമായ രക്തസ്രാവം"},
        {"id":18,"gender":"female","category":"ആർത്തവ രക്തസ്രാവം","weight":1,
         "text":"ഭാരിച്ച ആർത്തവ രക്തസ്രാവം (7 ദിവസത്തിൽ കൂടുതൽ) ഉണ്ടോ?",
         "hint":"ആർത്തവ ആരംഭം മുതൽ ഉള്ള ഭാരിച്ച ആർത്തവ രക്തസ്രാവം"},
        {"id":19,"gender":"female","category":"പ്രസവ രക്തസ്രാവം","weight":1,
         "text":"പ്രസവ ശേഷം അമിത രക്തസ്രാവം (>= 500 mL) ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"പ്രസവിച്ച രോഗികൾക്ക്; ബാധകമല്ലെങ്കിൽ ഒഴിവാക്കുക"},
        {"id":20,"gender":"female","category":"ഗർഭം","weight":1,
         "text":"ഭാരിച്ച രക്തസ്രാവവുമായി ബന്ധപ്പെട്ട ഗർഭഛിദ്രം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ഗർഭഛിദ്ര സമയത്ത് വൈദ്യ ഇടപെടൽ ആവശ്യമായ"},
        {"id":18,"gender":"male","category":"ഹീമോഫിലിയ","weight":2,
         "text":"പ്രകടമായ ആഘാതം ഇല്ലാതെ പേശികൾ/സന്ധികളിൽ രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ഹീമോഫിലിയയുടെ പ്രധാന ലക്ഷണം"},
        {"id":19,"gender":"male","category":"ഖതനം","weight":1,
         "text":"ഖതനം ശേഷം അമിത അല്ലെങ്കിൽ ദീർഘ രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ഖതനം ശേഷം അസാധാരണ രക്തസ്രാവം"},
        {"id":20,"gender":"male","category":"മൂത്ര രക്തസ്രാവം","weight":1,
         "text":"ഒന്നിലധികം തവണ അണുബാധ ഇല്ലാതെ മൂത്രത്തിൽ രക്തം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ആവർത്തിക്കുന്ന ഹിമാറ്റൂറിയ"},
        {"id":18,"gender":"other","category":"ഹോർമോൺ രക്തസ്രാവം","weight":1,
         "text":"ഹോർമോൺ മാറ്റങ്ങളുമായി ബന്ധപ്പെട്ട അസാധാരണ രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ബാധകമല്ലെങ്കിൽ ഒഴിവാക്കുക"},
        {"id":19,"gender":"other","category":"ശസ്ത്രക്രിയ സ്ഥലം","weight":1,
         "text":"ഏതെങ്കിലും ശസ്ത്രക്രിയ സ്ഥലത്ത് നിന്ന് ദീർഘ രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"ബയോപ്സി ഉൾപ്പെടെ ചെറിയ നടപടിക്രമങ്ങൾ"},
        {"id":20,"gender":"other","category":"ആവർത്തിക്കുന്ന രക്തസ്രാവം","weight":1,
         "text":"വൈദ്യ ശ്രദ്ധ ആവശ്യമുള്ള ആവർത്തിക്കുന്ന വിശദീകരിക്കാനാകാത്ത രക്തസ്രാവം ഉണ്ടായിട്ടുണ്ടോ?",
         "hint":"വ്യക്തമായ കാരണം ഇല്ലാതെ"},
    ],
    "Hindi": [
        {"id":1,"gender":"all","category":"चोट","weight":1,
         "text":"क्या आपको बिना किसी स्पष्ट कारण के आसानी से चोट लग जाती है?",
         "hint":"आघात से असंबंधित सहज चोट"},
        {"id":2,"gender":"all","category":"नाक से खून","weight":1,
         "text":"क्या आपको कभी 10 मिनट से अधिक समय तक नाक से खून आया है?",
         "hint":"बार-बार नाक से खून आना शामिल है"},
        {"id":3,"gender":"all","category":"मसूड़े","weight":1,
         "text":"क्या आपके मसूड़ों से टूथब्रश करते समय या अपने आप खून आता है?",
         "hint":"मुंह/मसूड़े से खून"},
        {"id":4,"gender":"all","category":"दंत प्रक्रिया","weight":1,
         "text":"क्या दांत निकालने के बाद आपको अत्यधिक खून आया है?",
         "hint":"दंत कार्य के बाद अतिरिक्त हस्तक्षेप की आवश्यकता"},
        {"id":5,"gender":"all","category":"सर्जरी","weight":1,
         "text":"क्या किसी सर्जरी के बाद आपको अत्यधिक रक्तस्राव हुआ है?",
         "hint":"ऑपरेशन के बाद अपेक्षा से अधिक रक्तस्राव"},
        {"id":6,"gender":"all","category":"रक्त आधान","weight":2,
         "text":"क्या रक्तस्राव के कारण आपको कभी रक्त चढ़ाने की आवश्यकता पड़ी है?",
         "hint":"सर्जरी नहीं, रक्तस्राव से संबंधित आधान"},
        {"id":7,"gender":"all","category":"आपातकालीन","weight":2,
         "text":"क्या आप कभी रक्तस्राव के कारण अस्पताल में भर्ती हुए हैं?",
         "hint":"नियोजित सर्जिकल प्रवेश को छोड़कर"},
        {"id":8,"gender":"all","category":"जोड़ों में खून","weight":2,
         "text":"क्या आपके किसी जोड़ में कभी रक्तस्राव हुआ है जिससे दर्द और सूजन हुई?",
         "hint":"आमतौर पर घुटने, कोहनी या टखने"},
        {"id":9,"gender":"all","category":"मांसपेशी","weight":2,
         "text":"क्या आपकी मांसपेशी के अंदर कभी गहरा रक्तस्राव हुआ है?",
         "hint":"अक्सर बिना किसी महत्वपूर्ण आघात के"},
        {"id":10,"gender":"all","category":"पेशाब में खून","weight":1,
         "text":"क्या आपने कभी मूत्र संक्रमण के बिना पेशाब में खून देखा है?",
         "hint":"संक्रमण से अस्पष्टीकृत हेमट्यूरिया"},
        {"id":11,"gender":"all","category":"पाचन","weight":1,
         "text":"क्या आपके मल में कभी खून आया है?",
         "hint":"पुष्टि जीआई रक्तस्राव"},
        {"id":12,"gender":"all","category":"पारिवारिक इतिहास","weight":1,
         "text":"क्या किसी करीबी परिवार के सदस्य को रक्तस्राव विकार का निदान किया गया है?",
         "hint":"जैसे हीमोफिलिया, VWD, प्लेटलेट विकार"},
        {"id":13,"gender":"all","category":"घाव","weight":1,
         "text":"क्या छोटे घावों से खून बंद होने में 15 मिनट से अधिक लगता है?",
         "hint":"छोटे घावों से असामान्य रक्तस्राव"},
        {"id":14,"gender":"all","category":"मस्तिष्क","weight":3,
         "text":"क्या आपको कभी मस्तिष्क में सहज रक्तस्राव हुआ है?",
         "hint":"आघात से असंबंधित ICH"},
        {"id":15,"gender":"all","category":"पेटेकिया","weight":1,
         "text":"क्या बिना चोट के आपकी त्वचा पर छोटे लाल धब्बे दिखते हैं?",
         "hint":"विशेष रूप से निचले अंगों पर"},
        {"id":16,"gender":"all","category":"एनीमिया","weight":1,
         "text":"क्या रक्तस्राव के कारण आयरन की कमी से एनीमिया हुआ?",
         "hint":"पुरानी रक्त हानि के कारण एनीमिया"},
        {"id":17,"gender":"all","category":"दवा रक्तस्राव","weight":1,
         "text":"क्या एस्पिरिन, NSAIDs लेते समय अत्यधिक रक्तस्राव होता है?",
         "hint":"एंटीप्लेटलेट दवाओं पर असमानुपातिक रक्तस्राव"},
        {"id":18,"gender":"female","category":"मासिक धर्म","weight":1,
         "text":"क्या आपको भारी मासिक रक्तस्राव होता है (7 दिन से अधिक)?",
         "hint":"मासिक धर्म की शुरुआत से भारी रक्तस्राव"},
        {"id":19,"gender":"female","category":"प्रसव","weight":1,
         "text":"क्या प्रसव के बाद अत्यधिक रक्तस्राव (>= 500 mL) हुआ है?",
         "hint":"जिन्होंने प्रसव किया है; लागू न हो तो छोड़ें"},
        {"id":20,"gender":"female","category":"गर्भावस्था","weight":1,
         "text":"क्या भारी रक्तस्राव के साथ गर्भपात हुआ है?",
         "hint":"गर्भपात के दौरान चिकित्सा हस्तक्षेप की आवश्यकता"},
        {"id":18,"gender":"male","category":"हीमोफिलिया","weight":2,
         "text":"क्या बिना स्पष्ट चोट के मांसपेशियों या जोड़ों में सहज रक्तस्राव हुआ है?",
         "hint":"हीमोफिलिया का विशिष्ट लक्षण"},
        {"id":19,"gender":"male","category":"खतना","weight":1,
         "text":"क्या खतने के बाद अत्यधिक रक्तस्राव हुआ था?",
         "hint":"खतने के बाद असामान्य रक्तस्राव"},
        {"id":20,"gender":"male","category":"मूत्र","weight":1,
         "text":"क्या एक से अधिक बार बिना संक्रमण के पेशाब में खून आया है?",
         "hint":"बार-बार हेमट्यूरिया"},
        {"id":18,"gender":"other","category":"हार्मोनल","weight":1,
         "text":"क्या हार्मोनल परिवर्तनों से संबंधित असामान्य रक्तस्राव हुआ है?",
         "hint":"लागू न हो तो छोड़ें"},
        {"id":19,"gender":"other","category":"सर्जिकल साइट","weight":1,
         "text":"क्या किसी सर्जिकल साइट से लंबे समय तक रक्तस्राव हुआ है?",
         "hint":"बायोप्सी सहित छोटी प्रक्रियाएं"},
        {"id":20,"gender":"other","category":"अज्ञात रक्तस्राव","weight":1,
         "text":"क्या बार-बार अज्ञात रक्तस्राव हुआ है जिसके लिए चिकित्सा ध्यान की आवश्यकता पड़ी?",
         "hint":"स्पष्ट कारण के बिना"},
    ],
    "Tamil": [
        {"id":1,"gender":"all","category":"காயம்","weight":1,
         "text":"தெளிவான காரணம் இல்லாமல் உங்களுக்கு எளிதில் காயங்கள் ஏற்படுகின்றனவா?",
         "hint":"அதிர்ச்சியுடன் தொடர்பில்லாத தன்னிச்சையான காயங்கள்"},
        {"id":2,"gender":"all","category":"மூக்கிலிருந்து இரத்தம்","weight":1,
         "text":"10 நிமிடங்களுக்கும் அதிகமாக மூக்கிலிருந்து இரத்தம் வந்ததுண்டா?",
         "hint":"மீண்டும் மீண்டும் வரும் மூக்கிலிருந்து இரத்தம் உட்பட"},
        {"id":3,"gender":"all","category":"வாய்","weight":1,
         "text":"பல் துலக்கும்போது அல்லது தன்னிச்சையாக ஈறுகளிலிருந்து இரத்தம் வருகிறதா?",
         "hint":"வாய்/ஈறு இரத்தப்போக்கு"},
        {"id":4,"gender":"all","category":"பல் சிகிச்சை","weight":1,
         "text":"பல் பிடுங்கிய பிறகு அதிகமாக இரத்தம் வந்ததுண்டா?",
         "hint":"பல் சிகிச்சைக்கு பிறகு கூடுதல் தலையீடு தேவைப்பட்ட"},
        {"id":5,"gender":"all","category":"அறுவை சிகிச்சை","weight":1,
         "text":"அறுவை சிகிச்சைக்குப் பிறகு நீண்ட நேரம் இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"எதிர்பார்த்ததை விட அதிக இரத்தப்போக்கு"},
        {"id":6,"gender":"all","category":"இரத்தம் ஏற்றல்","weight":2,
         "text":"இரத்தப்போக்கு காரணமாக இரத்தம் ஏற்ற வேண்டியிருந்ததுண்டா?",
         "hint":"அறுவை சிகிச்சை அல்ல, இரத்தப்போக்குடன் தொடர்புடைய"},
        {"id":7,"gender":"all","category":"அவசர சிகிச்சை","weight":2,
         "text":"இரத்தப்போக்கு காரணமாக மருத்துவமனையில் சேர்க்கப்பட்டதுண்டா?",
         "hint":"திட்டமிட்ட அறுவை சிகிச்சை சேர்க்கைகளை தவிர"},
        {"id":8,"gender":"all","category":"மூட்டு இரத்தப்போக்கு","weight":2,
         "text":"மூட்டுக்குள் இரத்தப்போக்கு ஏற்பட்டு வலி மற்றும் வீக்கம் உண்டானதுண்டா?",
         "hint":"பொதுவாக முழங்கால், முழங்கை அல்லது கணுக்கால்"},
        {"id":9,"gender":"all","category":"தசை ரத்தக்கட்டு","weight":2,
         "text":"தசைக்குள் ஆழமான இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"குறிப்பிடத்தக்க அதிர்ச்சி இல்லாமல்"},
        {"id":10,"gender":"all","category":"சிறுநீரில் இரத்தம்","weight":1,
         "text":"சிறுநீர் தொற்று இல்லாமல் சிறுநீரில் இரத்தம் கண்டதுண்டா?",
         "hint":"தொற்றால் விளக்க முடியாத ஹீமட்டூரியா"},
        {"id":11,"gender":"all","category":"குடல் இரத்தப்போக்கு","weight":1,
         "text":"மலத்தில் இரத்தம் வந்ததுண்டா?",
         "hint":"உறுதிப்படுத்தப்பட்ட GI இரத்தப்போக்கு"},
        {"id":12,"gender":"all","category":"குடும்ப வரலாறு","weight":1,
         "text":"நெருங்கிய குடும்ப உறுப்பினருக்கு இரத்தப்போக்கு கோளாறு இருப்பதாக கண்டறியப்பட்டதுண்டா?",
         "hint":"ஹீமோஃபிலியா, VWD, பிளேட்லெட் கோளாறு"},
        {"id":13,"gender":"all","category":"காயம் இரத்தப்போக்கு","weight":1,
         "text":"சிறிய காயங்களில் இரத்தம் நிறுத்த 15 நிமிடங்களுக்கும் அதிகமாக ஆகுமா?",
         "hint":"சிறிய காயங்களில் இருந்து அசாதாரண இரத்தப்போக்கு"},
        {"id":14,"gender":"all","category":"மூளை இரத்தப்போக்கு","weight":3,
         "text":"தன்னிச்சையான மூளை உள் இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"அதிர்ச்சியுடன் தொடர்பில்லாத ICH"},
        {"id":15,"gender":"all","category":"தோல் புள்ளிகள்","weight":1,
         "text":"காயம் இல்லாமல் தோலில் சிறிய சிவப்பு புள்ளிகள் தோன்றுகின்றனவா?",
         "hint":"குறிப்பாக கீழ் மூட்டுகளில்"},
        {"id":16,"gender":"all","category":"இரும்புச்சத்து குறைபாடு","weight":1,
         "text":"இரத்தப்போக்கு காரணமாக இரும்புச்சத்து குறைபாடு கண்டறியப்பட்டதுண்டா?",
         "hint":"நாள்பட்ட இரத்த இழப்பு காரணமான இரத்தசோகை"},
        {"id":17,"gender":"all","category":"மருந்து இரத்தப்போக்கு","weight":1,
         "text":"ஆஸ்பிரின், NSAIDs எடுக்கும்போது அதிகமாக இரத்தப்போக்கு ஏற்படுகிறதா?",
         "hint":"விகிதாசார இரத்தப்போக்கு"},
        {"id":18,"gender":"female","category":"மாதவிடாய்","weight":1,
         "text":"கனமான மாதவிடாய் இரத்தப்போக்கு உள்ளதா (7 நாட்களுக்கும் அதிகமாக)?",
         "hint":"மாதவிடாய் தொடக்கத்திலிருந்து கனமான இரத்தப்போக்கு"},
        {"id":19,"gender":"female","category":"பிரசவ இரத்தப்போக்கு","weight":1,
         "text":"பிரசவத்திற்குப் பிறகு அதிகப்படியான இரத்தப்போக்கு (>= 500 mL) ஏற்பட்டதுண்டா?",
         "hint":"பொருந்தவில்லை என்றால் தவிர்க்கவும்"},
        {"id":20,"gender":"female","category":"கர்ப்பகால இரத்தப்போக்கு","weight":1,
         "text":"கனமான இரத்தப்போக்குடன் கூடிய கருச்சிதைவு ஏற்பட்டதுண்டா?",
         "hint":"மருத்துவ தலையீடு தேவைப்பட்ட"},
        {"id":18,"gender":"male","category":"ஹீமோஃபிலியா","weight":2,
         "text":"தெளிவான காயம் இல்லாமல் தசைகள்/மூட்டுகளில் தன்னிச்சையான இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"ஹீமோஃபிலியாவின் முக்கிய அறிகுறி"},
        {"id":19,"gender":"male","category":"விருத்தசேதனம்","weight":1,
         "text":"விருத்தசேதனத்திற்குப் பிறகு அதிகப்படியான இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"விருத்தசேதனத்திற்கு பிறகு அசாதாரண இரத்தப்போக்கு"},
        {"id":20,"gender":"male","category":"சிறுநீர் இரத்தப்போக்கு","weight":1,
         "text":"ஒரு முறைக்கும் மேல் தொற்று இல்லாமல் சிறுநீரில் இரத்தம் வந்ததுண்டா?",
         "hint":"மீண்டும் மீண்டும் வரும் ஹீமட்டூரியா"},
        {"id":18,"gender":"other","category":"ஹார்மோன் இரத்தப்போக்கு","weight":1,
         "text":"ஹார்மோன் மாற்றங்களுடன் தொடர்புடைய அசாதாரண இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"பொருந்தவில்லை என்றால் தவிர்க்கவும்"},
        {"id":19,"gender":"other","category":"அறுவை சிகிச்சை தளம்","weight":1,
         "text":"அறுவை சிகிச்சை தளத்தில் இருந்து நீண்ட நேரம் இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"பயாப்ஸி உட்பட சிறிய செயல்முறைகள்"},
        {"id":20,"gender":"other","category":"மீண்டும் வரும் இரத்தப்போக்கு","weight":1,
         "text":"மருத்துவ கவனிப்பு தேவைப்பட்ட மீண்டும் மீண்டும் வரும் இரத்தப்போக்கு ஏற்பட்டதுண்டா?",
         "hint":"தெளிவான காரணம் இல்லாத"},
    ],
}

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');
:root{--bg:#0a0e1a;--surface:#111827;--surface2:#1a2236;--border:#1e2d45;
     --accent:#00c2cb;--accent2:#3b82f6;--red:#f43f5e;--amber:#f59e0b;
     --green:#10b981;--purple:#a855f7;--text:#e2e8f0;--muted:#64748b;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewContainer"]>section,
[data-testid="block-container"],.main,.block-container{background-color:var(--bg)!important;color:var(--text)!important;}
[data-testid="stHeader"]{background-color:var(--bg)!important;}
::-webkit-scrollbar{width:6px}::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
*,p,span,div,label{font-family:'Sora',sans-serif!important;color:var(--text);}
h1,h2,h3{font-family:'Crimson Pro',serif!important;color:var(--text)!important;}
.stProgress>div>div>div{background:linear-gradient(90deg,var(--accent2),var(--accent))!important;border-radius:99px;box-shadow:0 0 12px rgba(0,194,203,.4);}
.stProgress>div>div{background:var(--surface2)!important;border-radius:99px;height:8px!important;}
div.stButton>button{font-family:'Sora',sans-serif!important;font-weight:600!important;font-size:.95rem!important;border-radius:12px!important;padding:.65rem 1.5rem!important;border:1px solid var(--border)!important;background:var(--surface2)!important;color:var(--text)!important;transition:all .2s ease!important;box-shadow:0 2px 8px rgba(0,0,0,.3)!important;}
div.stButton>button:hover{background:var(--surface)!important;border-color:var(--accent)!important;color:var(--accent)!important;transform:translateY(-2px)!important;}
div.stButton>button[kind="primary"]{background:linear-gradient(135deg,#0e7490,var(--accent))!important;border:none!important;color:#fff!important;}
div.stButton>button[kind="primary"]:hover{background:linear-gradient(135deg,var(--accent),#0e7490)!important;color:#fff!important;transform:translateY(-3px)!important;}
.bat-card{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:2rem 1.8rem;box-shadow:0 0 40px rgba(0,194,203,.06),0 4px 32px rgba(0,0,0,.5);margin-bottom:1.4rem;position:relative;overflow:hidden;}
.bat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--accent),transparent);}
.hero-wrap{text-align:center;padding:2.5rem 1rem 1rem;}
.hero-icon{font-size:3.5rem;filter:drop-shadow(0 0 20px rgba(244,63,94,.6));margin-bottom:.4rem;animation:pulse-icon 2.5s ease-in-out infinite;}
@keyframes pulse-icon{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
.hero-title{font-family:'Crimson Pro',serif!important;font-size:2.4rem!important;font-weight:600!important;background:linear-gradient(135deg,#e2e8f0 30%,var(--accent));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:.2rem 0!important;line-height:1.2!important;}
.hero-sub{color:var(--muted)!important;font-size:1rem;max-width:500px;margin:.6rem auto 1.8rem;line-height:1.6;}
.pill-row{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;margin-bottom:1.8rem;}
.pill{background:var(--surface2);border:1px solid var(--border);border-radius:99px;padding:.35rem 1rem;font-size:.82rem;color:var(--muted)!important;display:inline-flex;align-items:center;gap:.4rem;}
.pill span{color:var(--accent)!important;font-weight:600;}
.q-label{font-size:.75rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)!important;margin-bottom:.5rem;}
.q-text{font-family:'Crimson Pro',serif!important;font-size:1.5rem!important;line-height:1.45;color:var(--text)!important;margin-bottom:.6rem!important;}
.q-hint{font-size:.84rem;color:var(--muted)!important;background:var(--surface2);border-left:3px solid var(--accent2);border-radius:0 8px 8px 0;padding:.5rem .9rem;}
.step-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:.5rem;}
.step-label{color:var(--muted)!important;font-size:.82rem;}
.step-num{color:var(--accent)!important;font-size:.82rem;font-weight:600;}
.glow-divider{border:none;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1rem 0;}
.stat-bar{display:flex;justify-content:space-around;background:var(--surface2);border:1px solid var(--border);border-radius:14px;padding:1rem;margin-bottom:1.2rem;}
.stat-item{text-align:center;}
.stat-val{font-size:1.6rem;font-weight:700;font-family:'Crimson Pro',serif!important;line-height:1;}
.stat-lbl{font-size:.75rem;color:var(--muted)!important;margin-top:.2rem;}
.result-row{display:flex;align-items:flex-start;gap:.8rem;padding:.65rem 0;border-bottom:1px solid var(--border);font-size:.88rem;}
.result-row:last-child{border-bottom:none;}
.r-qnum{min-width:2rem;font-size:.75rem;color:var(--muted)!important;padding-top:.1rem;font-weight:600;}
.r-text{flex:1;color:#cbd5e1!important;line-height:1.4;}
.r-ans{min-width:3rem;text-align:right;font-weight:700;font-size:.88rem;}
.cat-tag{display:inline-flex;align-items:center;gap:.3rem;border-radius:8px;padding:.3rem .75rem;margin:.2rem;font-size:.82rem;font-weight:500;}
.disclaimer{background:linear-gradient(135deg,#1c1a05,#292400);border:1px solid #ca8a04;border-radius:12px;padding:1rem 1.2rem;font-size:.83rem;color:#fbbf24!important;margin-top:1.5rem;line-height:1.5;}
.score-ring{width:130px;height:130px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;margin:0 auto 1rem;}
.score-big{font-family:'Crimson Pro',serif!important;font-size:2.8rem!important;font-weight:700!important;line-height:1!important;}
.score-of{font-size:.85rem;color:var(--muted)!important;}
.risk-badge{display:inline-flex;align-items:center;gap:.5rem;border-radius:99px;padding:.5rem 1.4rem;font-weight:700;font-size:1rem;margin-bottom:.8rem;}
.advice-text{font-size:.92rem;color:#94a3b8!important;line-height:1.6;text-align:center;max-width:480px;margin:0 auto;}
.info-field{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:.7rem 1rem;margin-bottom:.5rem;display:flex;justify-content:space-between;align-items:center;}
.info-label{color:var(--muted)!important;font-size:.8rem;}
.info-val{color:var(--accent)!important;font-weight:600;font-size:.9rem;}
div[data-baseweb="select"]>div{background:var(--surface2)!important;border-color:var(--border)!important;color:var(--text)!important;border-radius:10px!important;}
div[data-baseweb="select"] *{color:var(--text)!important;}
div[data-baseweb="popover"] *{background:var(--surface)!important;color:var(--text)!important;}
input[type="text"],input[type="number"],.stTextInput input,.stNumberInput input{background:var(--surface2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:10px!important;}
.stDateInput input{background:var(--surface2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:10px!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def get_questions(lang, gender_label):
    gender_map = {
        "♂  Male":"male","♀  Female":"female","⚧  Other / Prefer not to say":"other",
        "♂  പുരുഷൻ":"male","♀  സ്ത്രീ":"female","⚧  മറ്റുള്ളവർ":"other",
        "♂  पुरुष":"male","♀  महिला":"female","⚧  अन्य":"other",
        "♂  ஆண்":"male","♀  பெண்":"female","⚧  மற்றவர்கள்":"other",
    }
    gk   = gender_map.get(gender_label, "other")
    pool = QUESTIONS.get(lang, QUESTIONS["English"])
    return [q for q in pool if q["gender"] == "all"] + \
           [q for q in pool if q["gender"] == gk]

def classify(ws, t):
    if ws == 0:
        return {"label":t["risk_low"],"color":"#10b981","bg":"linear-gradient(135deg,#022c22,#064e3b)",
                "ring":"rgba(16,185,129,0.25)","icon":"✅","advice":t["adv_low"],"risk_en":"Low Risk"}
    elif ws <= 3:
        return {"label":t["risk_mild"],"color":"#f59e0b","bg":"linear-gradient(135deg,#1c1005,#292100)",
                "ring":"rgba(245,158,11,0.25)","icon":"⚠️","advice":t["adv_mild"],"risk_en":"Borderline / Mild"}
    elif ws <= 6:
        return {"label":t["risk_mod"],"color":"#f43f5e","bg":"linear-gradient(135deg,#1f0a10,#4c0519)",
                "ring":"rgba(244,63,94,0.25)","icon":"🔴","advice":t["adv_mod"],"risk_en":"Moderate Risk"}
    else:
        return {"label":t["risk_high"],"color":"#a855f7","bg":"linear-gradient(135deg,#1a0a2e,#3b0764)",
                "ring":"rgba(168,85,247,0.25)","icon":"🚨","advice":t["adv_high"],"risk_en":"High Risk — Urgent"}

def go_to(p): st.session_state.page = p

# ── Chart builder ─────────────────────────────────────────────────────────────
def make_charts(questions, answers, yes_count, no_count, total_ans, weighted, result, t):
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
    fig.patch.set_facecolor("#111827")
    risk_color = result["color"]

    # ── 1. Donut — Yes vs No ──
    ax1 = axes[0]
    ax1.set_facecolor("#111827")
    sizes  = [yes_count, max(no_count,0), max(total_ans - yes_count - no_count, 0)]
    clrs   = [risk_color, "#10b981", "#1e2d45"]
    labels = [t["positive"], t["negative"], "—"]
    wedges, _ = ax1.pie(
        [s for s in sizes if s > 0],
        colors=[clrs[i] for i,s in enumerate(sizes) if s > 0],
        startangle=90, wedgeprops=dict(width=0.55, edgecolor="#111827", linewidth=2)
    )
    ax1.text(0, 0.08, str(yes_count), ha="center", va="center",
             fontsize=22, fontweight="bold", color=risk_color)
    ax1.text(0,-0.25, f"{t['of']} {total_ans}", ha="center", va="center",
             fontsize=10, color="#64748b")
    ax1.set_title(t["positive"] + " / " + t["negative"],
                  color="#e2e8f0", fontsize=11, pad=10)
    patches = [mpatches.Patch(color=clrs[i], label=labels[i])
               for i,s in enumerate(sizes) if s > 0]
    ax1.legend(handles=patches, loc="lower center", fontsize=8,
               facecolor="#1a2236", edgecolor="#1e2d45",
               labelcolor="#e2e8f0", ncol=2, bbox_to_anchor=(0.5,-0.12))

    # ── 2. Gauge — Weighted score ──
    ax2 = axes[1]
    ax2.set_facecolor("#111827")
    max_score = sum(q["weight"] for q in questions)
    theta_start, theta_end = np.pi, 0
    theta = np.linspace(theta_start, theta_end, 300)
    zones = [(0,3,"#10b981"),(3,6,"#f59e0b"),(6,10,"#f43f5e"),(10,max_score+1,"#a855f7")]
    for zs, ze, zc in zones:
        t_s = theta_start - (zs/max(max_score,1))*(theta_start-theta_end)
        t_e = theta_start - (min(ze,max_score)/max(max_score,1))*(theta_start-theta_end)
        th  = np.linspace(t_s, t_e, 100)
        ax2.fill_between(np.cos(th), np.sin(th)*0,
                         np.cos(th)*0.0+np.cos(th), alpha=0)
        ax2.plot(np.cos(th)*0.85, np.sin(th)*0.85, color=zc, lw=18, alpha=0.35, solid_capstyle="butt")
    needle_angle = theta_start - (min(weighted,max_score)/max(max_score,1))*(theta_start-theta_end)
    ax2.annotate("", xy=(np.cos(needle_angle)*0.72, np.sin(needle_angle)*0.72),
                 xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=risk_color, lw=2.5,
                                 mutation_scale=18))
    ax2.add_patch(plt.Circle((0,0), 0.06, color=risk_color, zorder=5))
    ax2.text(0, -0.25, str(weighted), ha="center", va="center",
             fontsize=20, fontweight="bold", color=risk_color)
    ax2.text(0, -0.48, t["weighted"], ha="center", va="center",
             fontsize=9, color="#64748b")
    ax2.set_xlim(-1.1, 1.1); ax2.set_ylim(-0.6, 1.15)
    ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title(t["chart_title"], color="#e2e8f0", fontsize=11, pad=10)

    # ── 3. Horizontal bar — symptoms by category ──
    ax3 = axes[2]
    ax3.set_facecolor("#111827")
    pos_cats  = [q["category"] for i,q in enumerate(questions) if answers.get(i)=="Yes"]
    all_cats  = list(dict.fromkeys(q["category"] for q in questions))
    yes_counts_cat = [pos_cats.count(c) for c in all_cats]
    bar_colors = [risk_color if yc>0 else "#1e2d45" for yc in yes_counts_cat]
    bars = ax3.barh(all_cats, yes_counts_cat, color=bar_colors,
                    height=0.55, edgecolor="#111827", linewidth=0.5)
    ax3.set_facecolor("#111827")
    ax3.tick_params(colors="#64748b", labelsize=7.5)
    ax3.spines["top"].set_visible(False); ax3.spines["right"].set_visible(False)
    ax3.spines["bottom"].set_color("#1e2d45"); ax3.spines["left"].set_color("#1e2d45")
    ax3.set_xlim(0, 1.5)
    ax3.set_xticks([0,1])
    ax3.xaxis.label.set_color("#64748b")
    for lbl in ax3.get_yticklabels(): lbl.set_color("#94a3b8")
    for lbl in ax3.get_xticklabels(): lbl.set_color("#64748b")
    ax3.set_title(t["pos_domains"].replace("🔴 ",""), color="#e2e8f0", fontsize=11, pad=10)

    plt.tight_layout(pad=2.0)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=140, bbox_inches="tight",
                facecolor="#111827", edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf

# ── PDF builder ───────────────────────────────────────────────────────────────
def build_pdf(patient, questions, answers, yes_count, total_ans, weighted, result, t, chart_buf):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    NAVY   = colors.HexColor("#0a0e1a")
    TEAL   = colors.HexColor("#00c2cb")
    SLATE  = colors.HexColor("#1a2236")
    BORDER = colors.HexColor("#1e2d45")
    LIGHT  = colors.HexColor("#e2e8f0")
    MUTED  = colors.HexColor("#64748b")
    RISK_C = colors.HexColor(result["color"])
    YES_C  = colors.HexColor("#f43f5e")
    NO_C   = colors.HexColor("#10b981")

    styles = getSampleStyleSheet()
    def sty(name, **kw):
        s = ParagraphStyle(name, **kw)
        return s

    S_title   = sty("T", fontSize=22, textColor=TEAL,      fontName="Helvetica-Bold",
                    alignment=TA_CENTER, spaceAfter=4)
    S_sub     = sty("Su",fontSize=9,  textColor=MUTED,     fontName="Helvetica",
                    alignment=TA_CENTER, spaceAfter=12)
    S_sect    = sty("Se",fontSize=11, textColor=TEAL,      fontName="Helvetica-Bold",
                    spaceBefore=14, spaceAfter=6)
    S_body    = sty("B", fontSize=9,  textColor=LIGHT,     fontName="Helvetica",
                    leading=14, spaceAfter=4)
    S_advice  = sty("A", fontSize=9,  textColor=LIGHT,     fontName="Helvetica-Oblique",
                    leading=13, spaceAfter=4)
    S_risk    = sty("R", fontSize=14, textColor=RISK_C,    fontName="Helvetica-Bold",
                    alignment=TA_CENTER, spaceAfter=6)
    S_footer  = sty("F", fontSize=7.5,textColor=MUTED,     fontName="Helvetica-Oblique",
                    alignment=TA_CENTER, spaceBefore=12)
    S_q       = sty("Q", fontSize=8,  textColor=LIGHT,     fontName="Helvetica", leading=12)
    S_yes     = sty("Y", fontSize=8,  textColor=YES_C,     fontName="Helvetica-Bold")
    S_no      = sty("N", fontSize=8,  textColor=NO_C,      fontName="Helvetica-Bold")
    S_na      = sty("NA",fontSize=8,  textColor=MUTED,     fontName="Helvetica")

    story = []

    # Header
    story.append(Paragraph(t["pdf_title"], S_title))
    story.append(Paragraph("International Society on Thrombosis and Haemostasis · Bleeding Assessment Tool", S_sub))
    story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=10))

    # Patient info table
    story.append(Paragraph(t["pdf_patient"], S_sect))
    pt_data = [
        [t["pdf_name"],   patient["name"],   t["pdf_date"],   patient["date"]],
        [t["pdf_age"],    str(patient["age"]) + " yrs",
         t["pdf_gender"], patient["gender"]],
        [t["pdf_id"],     patient.get("pid","—"), "", ""],
    ]
    pt_table = Table(pt_data, colWidths=[3*cm, 6*cm, 3*cm, 5*cm])
    pt_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,-1), SLATE),
        ("TEXTCOLOR",   (0,0),(0,-1),  MUTED),
        ("TEXTCOLOR",   (2,0),(2,-1),  MUTED),
        ("TEXTCOLOR",   (1,0),(1,-1),  LIGHT),
        ("TEXTCOLOR",   (3,0),(3,-1),  LIGHT),
        ("FONTNAME",    (0,0),(0,-1),  "Helvetica"),
        ("FONTNAME",    (2,0),(2,-1),  "Helvetica"),
        ("FONTNAME",    (1,0),(1,-1),  "Helvetica-Bold"),
        ("FONTNAME",    (3,0),(3,-1),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 9),
        ("PADDING",     (0,0),(-1,-1), 6),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[SLATE, colors.HexColor("#1e2a3e"), SLATE]),
        ("GRID",        (0,0),(-1,-1), 0.5, BORDER),
        ("ROUNDEDCORNERS",[4]),
    ]))
    story.append(pt_table)
    story.append(Spacer(1, 10))

    # Score summary
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8))
    story.append(Paragraph(t["pdf_score"], S_sect))
    sc_data = [
        [t["positive"], t["negative"], t["answered"], t["weighted"]],
        [str(yes_count), str(total_ans-yes_count), str(total_ans), str(weighted)],
    ]
    sc_table = Table(sc_data, colWidths=["25%","25%","25%","25%"])
    sc_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0),  colors.HexColor("#0e7490")),
        ("BACKGROUND",  (0,1),(-1,1),  SLATE),
        ("TEXTCOLOR",   (0,0),(-1,0),  LIGHT),
        ("TEXTCOLOR",   (0,1),(-1,1),  TEAL),
        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTNAME",    (0,1),(-1,1),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,0),  9),
        ("FONTSIZE",    (0,1),(-1,1),  16),
        ("ALIGN",       (0,0),(-1,-1), "CENTER"),
        ("VALIGN",      (0,0),(-1,-1), "MIDDLE"),
        ("PADDING",     (0,0),(-1,-1), 8),
        ("GRID",        (0,0),(-1,-1), 0.5, BORDER),
    ]))
    story.append(sc_table)
    story.append(Spacer(1, 10))

    # Risk
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8))
    story.append(Paragraph(t["pdf_risk"], S_sect))
    story.append(Paragraph(f"{result['icon']}  {result['label']}", S_risk))
    story.append(Paragraph(f"<b>{t['pdf_advice']}:</b> {result['advice']}", S_advice))
    story.append(Spacer(1, 6))

    # Chart image
    if chart_buf:
        from reportlab.platypus import Image as RLImage
        chart_buf.seek(0)
        img = RLImage(chart_buf, width=17*cm, height=5.5*cm)
        story.append(img)
        story.append(Spacer(1, 8))

    # Positive domains
    pos_cats = [questions[i]["category"] for i,v in answers.items() if v=="Yes" and i<len(questions)]
    if pos_cats:
        story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8))
        story.append(Paragraph(t["pdf_domains"], S_sect))
        cat_text = "  ●  ".join(pos_cats)
        story.append(Paragraph(cat_text, S_body))
        story.append(Spacer(1, 6))

    # Detailed answers
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8))
    story.append(Paragraph(t["pdf_answers"], S_sect))

    ans_data = [["#", "Question / Category", "Answer"]]
    for i, q in enumerate(questions):
        ans = answers.get(i, "—")
        ans_data.append([
            str(i+1),
            f"{q['category']}: {q['text']}",
            t["pdf_yes"] if ans=="Yes" else (t["pdf_no"] if ans=="No" else t["pdf_na"])
        ])

    ans_table = Table(ans_data, colWidths=[1*cm, 13.5*cm, 2.5*cm])
    ts = TableStyle([
        ("BACKGROUND",  (0,0),(-1,0),  colors.HexColor("#0e7490")),
        ("TEXTCOLOR",   (0,0),(-1,0),  LIGHT),
        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,0),  8),
        ("ALIGN",       (0,0),(0,-1),  "CENTER"),
        ("ALIGN",       (2,0),(2,-1),  "CENTER"),
        ("FONTSIZE",    (0,1),(-1,-1), 8),
        ("PADDING",     (0,0),(-1,-1), 5),
        ("GRID",        (0,0),(-1,-1), 0.4, BORDER),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[SLATE, colors.HexColor("#1e2a3e")]),
    ])
    for i, (idx, q) in enumerate(zip(range(len(questions)), questions), start=1):
        ans = answers.get(idx-1, "—")
        if ans == "Yes":
            ts.add("TEXTCOLOR", (2,i),(2,i), YES_C)
            ts.add("FONTNAME",  (2,i),(2,i), "Helvetica-Bold")
        elif ans == "No":
            ts.add("TEXTCOLOR", (2,i),(2,i), NO_C)
        else:
            ts.add("TEXTCOLOR", (2,i),(2,i), MUTED)
        ts.add("TEXTCOLOR", (1,i),(1,i), LIGHT)
        ts.add("TEXTCOLOR", (0,i),(0,i), MUTED)
    ans_table.setStyle(ts)
    story.append(ans_table)

    # Footer
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceBefore=12, spaceAfter=6))
    story.append(Paragraph(t["pdf_footer"], S_footer))
    story.append(Paragraph(f"Generated: {patient['date']}  |  ISTH BAT Clinical Screening Tool", S_footer))

    doc.build(story)
    buf.seek(0)
    return buf

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
for k,v in [("page",0),("answers",{}),("lang","English"),
            ("gender",None),("questions",[]),
            ("pt_name",""),("pt_age",0),("pt_date",str(datetime.date.today())),("pt_id","")]:
    if k not in st.session_state: st.session_state[k] = v

# ── Language bar ──────────────────────────────────────────────────────────────
lang_opts = ["English","Malayalam","Hindi","Tamil"]
c1,c2,c3 = st.columns([3,2,3])
with c2:
    chosen = st.selectbox(T[st.session_state.lang]["lang_label"], lang_opts,
                          index=lang_opts.index(st.session_state.lang),
                          key="lang_sel", label_visibility="collapsed")
    if chosen != st.session_state.lang:
        st.session_state.lang=chosen; st.session_state.page=0
        st.session_state.answers={}; st.session_state.gender=None
        st.rerun()

t    = T[st.session_state.lang]
lang = st.session_state.lang

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 0 — INTRO
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == 0:
    st.markdown(f"""
    <div class='hero-wrap'>
        <div class='hero-icon'>🩸</div>
        <h1 class='hero-title'>{t['app_title']}</h1>
        <p class='hero-sub'>{t['app_sub']}</p>
        <div class='pill-row'>
            <div class='pill'>🗒️ <span>20</span> {t['pill_q']}</div>
            <div class='pill'>⏱️ <span>3-5</span> {t['pill_min']}</div>
            <div class='pill'>📊 {t['pill_result']}</div>
            <div class='pill'>🏥 {t['pill_isth']}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,4,1])
    with col2:
        st.markdown(f"""
        <div class='bat-card'>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;'>
                <div style='background:#1a2236;border-radius:12px;padding:1rem;border:1px solid #1e2d45;'>
                    <div style='color:#00c2cb;font-size:1.3rem;margin-bottom:.4rem;'>🎯</div>
                    <div style='font-weight:600;font-size:.9rem;margin-bottom:.3rem;'>{t['purpose_title']}</div>
                    <div style='color:#64748b;font-size:.82rem;line-height:1.5;'>{t['purpose_body']}</div>
                </div>
                <div style='background:#1a2236;border-radius:12px;padding:1rem;border:1px solid #1e2d45;'>
                    <div style='color:#3b82f6;font-size:1.3rem;margin-bottom:.4rem;'>📋</div>
                    <div style='font-weight:600;font-size:.9rem;margin-bottom:.3rem;'>{t['instr_title']}</div>
                    <div style='color:#64748b;font-size:.82rem;line-height:1.5;'>{t['instr_body']}</div>
                </div>
                <div style='background:#1a2236;border-radius:12px;padding:1rem;border:1px solid #1e2d45;'>
                    <div style='color:#f59e0b;font-size:1.3rem;margin-bottom:.4rem;'>⚖️</div>
                    <div style='font-weight:600;font-size:.9rem;margin-bottom:.3rem;'>{t['score_title']}</div>
                    <div style='color:#64748b;font-size:.82rem;line-height:1.5;'>{t['score_body']}</div>
                </div>
                <div style='background:#1a2236;border-radius:12px;padding:1rem;border:1px solid #1e2d45;'>
                    <div style='color:#10b981;font-size:1.3rem;margin-bottom:.4rem;'>🏥</div>
                    <div style='font-weight:600;font-size:.9rem;margin-bottom:.3rem;'>{t['outcome_title']}</div>
                    <div style='color:#64748b;font-size:.82rem;line-height:1.5;'>{t['outcome_body']}</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        if st.button(t["proceed"], use_container_width=True, type="primary"):
            go_to(1); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — PATIENT INFO
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == 1:
    col1,col2,col3 = st.columns([1,5,1])
    with col2:
        st.markdown(f"""
        <div style='text-align:center;padding:1.5rem 0 1rem;'>
            <div style='font-size:2.5rem;'>🏥</div>
            <h2 style='margin:.3rem 0;'>{t['patient_heading']}</h2>
            <p style='color:#64748b;font-size:.9rem;'>{t['patient_sub']}</p>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='bat-card'>", unsafe_allow_html=True)

        name = st.text_input(t["pt_name"], value=st.session_state.pt_name,
                             placeholder=t["pt_name_ph"])
        c1,c2b = st.columns(2)
        with c1:
            age  = st.number_input(t["pt_age"], min_value=0, max_value=120,
                                   value=int(st.session_state.pt_age) if st.session_state.pt_age else 0)
        with c2b:
            date = st.date_input(t["pt_date"],
                                 value=datetime.date.today())
        pid = st.text_input(t["pt_id"], value=st.session_state.pt_id,
                            placeholder=t["pt_id_ph"])

        st.markdown("</div>", unsafe_allow_html=True)

        err = False
        if not name.strip():
            st.markdown(f"<p style='color:#f59e0b;font-size:.85rem;'>{t['name_required']}</p>",
                        unsafe_allow_html=True)
            err = True
        if age < 1 or age > 120:
            st.markdown(f"<p style='color:#f59e0b;font-size:.85rem;'>{t['age_required']}</p>",
                        unsafe_allow_html=True)
            err = True

        bb1,bb2 = st.columns(2)
        with bb1:
            if st.button(t["back"], use_container_width=True):
                go_to(0); st.rerun()
        with bb2:
            if st.button(t["next_gender"], use_container_width=True, type="primary"):
                if not err:
                    st.session_state.pt_name = name.strip()
                    st.session_state.pt_age  = age
                    st.session_state.pt_date = str(date)
                    st.session_state.pt_id   = pid.strip()
                    go_to(2); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — GENDER SELECTION
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == 2:
    col1,col2,col3 = st.columns([1,4,1])
    with col2:
        st.markdown(f"""
        <div style='text-align:center;padding:1.5rem 0 1rem;'>
            <div style='font-size:2.5rem;'>⚧</div>
            <h2 style='margin:.3rem 0;'>{t['gender_heading']}</h2>
            <p style='color:#64748b;font-size:.9rem;'>{t['gender_sub']}</p>
        </div>""", unsafe_allow_html=True)

        g_opts   = [t["male"], t["female"], t["other"]]
        g_icons  = ["♂","♀","⚧"]
        g_colors = ["#3b82f6","#ec4899","#a855f7"]
        g_descs  = {
            "English":  ["Includes haemophilia-related and GU-specific questions",
                         "Includes menorrhagia, postpartum and pregnancy-related questions",
                         "Covers a broad range of general bleeding symptoms"],
            "Malayalam":["ഹീമോഫിലിയ, GU ചോദ്യങ്ങൾ ഉൾപ്പെടും",
                         "ആർത്തവ, പ്രസവ, ഗർഭ-ബന്ധിത ചോദ്യങ്ങൾ",
                         "പൊതു രക്തസ്രാവ ലക്ഷണ ചോദ്യങ്ങൾ"],
            "Hindi":    ["हीमोफिलिया और GU प्रश्न शामिल होंगे",
                         "मासिक धर्म, प्रसव, गर्भावस्था प्रश्न",
                         "सामान्य रक्तस्राव लक्षण प्रश्न"],
            "Tamil":    ["ஹீமோஃபிலியா மற்றும் GU கேள்விகள்",
                         "மாதவிடாய், பிரசவம், கர்ப்பகால கேள்விகள்",
                         "பொது இரத்தப்போக்கு அறிகுறி கேள்விகள்"],
        }
        descs = g_descs.get(lang, g_descs["English"])

        for i,(opt,icon,color,desc) in enumerate(zip(g_opts,g_icons,g_colors,descs)):
            st.markdown(f"""
            <div style='background:#1a2236;border:1px solid #1e2d45;border-radius:16px;
                 padding:1.1rem 1.3rem;margin-bottom:.6rem;display:flex;align-items:center;gap:1.2rem;'>
                <div style='font-size:2.2rem;width:3rem;text-align:center;
                     filter:drop-shadow(0 0 8px {color}88);'>{icon}</div>
                <div style='flex:1;'>
                    <div style='font-weight:700;font-size:1rem;color:{color};'>{opt}</div>
                    <div style='font-size:.82rem;color:#64748b;margin-top:.2rem;'>{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button(opt, use_container_width=True, key=f"g_{i}"):
                st.session_state.gender    = opt
                st.session_state.answers   = {}
                st.session_state.questions = get_questions(lang, opt)
                go_to(3); st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(t["back"], use_container_width=True):
            go_to(1); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGES 3 … N+2 — QUESTIONS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page >= 3:
    questions   = st.session_state.questions
    total       = len(questions)
    result_page = total + 3

    if st.session_state.page < result_page:
        q_idx = st.session_state.page - 3
        if q_idx >= total: go_to(result_page); st.rerun()
        q = questions[q_idx]

        st.markdown(f"""
        <div class='step-row'>
            <span class='step-label'>{t['isth_label']} &nbsp;·&nbsp;
              <span style='color:#a855f7;font-size:.78rem;'>{st.session_state.gender or ""}</span></span>
            <span class='step-num'>{t['question']} {q_idx+1} {t['of']} {total}</span>
        </div>""", unsafe_allow_html=True)
        st.progress(q_idx / total)
        st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)

        # Patient info strip
        st.markdown(f"""
        <div style='background:#1a2236;border:1px solid #1e2d45;border-radius:12px;
             padding:.6rem 1.2rem;margin-bottom:.9rem;display:flex;gap:2rem;flex-wrap:wrap;'>
            <span style='font-size:.8rem;color:#64748b;'>{t['pt_name']}: 
              <strong style='color:#00c2cb;'>{st.session_state.pt_name}</strong></span>
            <span style='font-size:.8rem;color:#64748b;'>{t['pt_age']}: 
              <strong style='color:#00c2cb;'>{st.session_state.pt_age}</strong></span>
            <span style='font-size:.8rem;color:#64748b;'>{t['pt_date']}: 
              <strong style='color:#00c2cb;'>{st.session_state.pt_date}</strong></span>
        </div>""", unsafe_allow_html=True)

        col1,col2,col3 = st.columns([1,6,1])
        with col2:
            st.markdown(f"""
            <div class='bat-card'>
                <div class='q-label'>{t['question']} {q_idx+1} &nbsp;·&nbsp; {q['category']}</div>
                <div class='q-text'>{q['text']}</div>
                <hr class='glow-divider'>
                <div class='q-hint'>ℹ️&nbsp;&nbsp;{q['hint']}</div>
            </div>""", unsafe_allow_html=True)

            prev = st.session_state.answers.get(q_idx)
            c1,c2b = st.columns(2)
            with c1:
                lbl = t["yes_sel"] if prev=="Yes" else t["yes"]
                if st.button(lbl, use_container_width=True,
                             type="primary" if prev=="Yes" else "secondary",
                             key=f"yes_{q_idx}"):
                    st.session_state.answers[q_idx]="Yes"
                    go_to(st.session_state.page+1); st.rerun()
            with c2b:
                lbl = t["no_sel"] if prev=="No" else t["no"]
                if st.button(lbl, use_container_width=True,
                             type="primary" if prev=="No" else "secondary",
                             key=f"no_{q_idx}"):
                    st.session_state.answers[q_idx]="No"
                    go_to(st.session_state.page+1); st.rerun()

            st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)
            n1,n2,n3 = st.columns([2,3,2])
            with n1:
                if st.session_state.page > 3:
                    if st.button(t["back"], use_container_width=True):
                        go_to(st.session_state.page-1); st.rerun()
            with n3:
                if q_idx in st.session_state.answers:
                    if st.button(t["skip"], use_container_width=True):
                        go_to(st.session_state.page+1); st.rerun()

            dots = "<div style='display:flex;gap:4px;justify-content:center;margin-top:1.2rem;flex-wrap:wrap;'>"
            for i in range(total):
                ans = st.session_state.answers.get(i)
                if i==q_idx:        c="#00c2cb"
                elif ans=="Yes":    c="#f43f5e"
                elif ans=="No":     c="#10b981"
                else:               c="#1e2d45"
                dots += f"<div style='width:10px;height:10px;border-radius:50%;background:{c};'></div>"
            dots += "</div>"
            st.markdown(dots, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # RESULTS PAGE
    # ══════════════════════════════════════════════════════════════════════════
    else:
        questions  = st.session_state.questions
        answers    = st.session_state.answers
        yes_count  = sum(1 for v in answers.values() if v=="Yes")
        no_count   = sum(1 for v in answers.values() if v=="No")
        total_ans  = len(answers)
        weighted   = sum(questions[i]["weight"] for i,v in answers.items()
                         if v=="Yes" and i<len(questions))
        result     = classify(weighted, t)
        c          = result["color"]
        patient    = {"name":st.session_state.pt_name,"age":st.session_state.pt_age,
                      "date":st.session_state.pt_date,"pid":st.session_state.pt_id,
                      "gender":st.session_state.gender or "—"}

        st.markdown(f"""
        <div style='text-align:center;padding:1.5rem 0 .5rem;'>
            <div style='font-size:2.2rem;'>📊</div>
            <h1 style='margin:.2rem 0;'>{t['results_title']}</h1>
            <p style='color:#64748b;font-size:.9rem;'>{t['results_sub']}</p>
        </div>""", unsafe_allow_html=True)

        # Patient summary strip
        st.markdown(f"""
        <div style='background:#1a2236;border:1px solid #1e2d45;border-radius:14px;
             padding:.9rem 1.4rem;margin-bottom:1rem;display:flex;gap:2rem;flex-wrap:wrap;align-items:center;'>
            <span style='font-size:.85rem;color:#64748b;'>👤 
              <strong style='color:#e2e8f0;'>{st.session_state.pt_name}</strong></span>
            <span style='font-size:.85rem;color:#64748b;'>🎂 
              <strong style='color:#e2e8f0;'>{st.session_state.pt_age} yrs</strong></span>
            <span style='font-size:.85rem;color:#64748b;'>📅 
              <strong style='color:#e2e8f0;'>{st.session_state.pt_date}</strong></span>
            <span style='font-size:.85rem;color:#64748b;'>{t['gender_badge']}: 
              <strong style='color:#a855f7;'>{st.session_state.gender or "—"}</strong></span>
            {f'<span style="font-size:.85rem;color:#64748b;">ID: <strong style="color:#00c2cb;">{st.session_state.pt_id}</strong></span>' if st.session_state.pt_id else ""}
        </div>""", unsafe_allow_html=True)

        col1,col2,col3 = st.columns([1,6,1])
        with col2:
            # Stats bar
            st.markdown(f"""
            <div class='stat-bar'>
                <div class='stat-item'><div class='stat-val' style='color:{c};'>{yes_count}</div>
                    <div class='stat-lbl'>{t['positive']}</div></div>
                <div class='stat-item'><div class='stat-val' style='color:#10b981;'>{no_count}</div>
                    <div class='stat-lbl'>{t['negative']}</div></div>
                <div class='stat-item'><div class='stat-val' style='color:#3b82f6;'>{total_ans}</div>
                    <div class='stat-lbl'>{t['answered']}</div></div>
                <div class='stat-item'><div class='stat-val' style='color:{c};'>{weighted}</div>
                    <div class='stat-lbl'>{t['weighted']}</div></div>
            </div>""", unsafe_allow_html=True)

            # Risk card
            st.markdown(f"""
            <div class='bat-card' style='text-align:center;background:{result["bg"]};border-color:{c}44;'>
                <div class='score-ring' style='background:radial-gradient(circle,{result["ring"]} 0%,transparent 70%);border:3px solid {c};'>
                    <div class='score-big' style='color:{c};'>{yes_count}</div>
                    <div class='score-of'>{t['of']} {total_ans}</div>
                </div>
                <div class='risk-badge' style='background:{c}22;color:{c};border:1px solid {c}55;'>
                    {result["icon"]} &nbsp; {result["label"]}
                </div>
                <p class='advice-text'>{result["advice"]}</p>
            </div>""", unsafe_allow_html=True)

            # ── CHARTS ──────────────────────────────────────────────────────
            st.markdown(f"#### 📈 {t['chart_title']}")
            chart_buf = make_charts(questions, answers, yes_count, no_count,
                                    total_ans, weighted, result, t)
            st.image(chart_buf, use_container_width=True)
            chart_buf.seek(0)

            # Positive categories
            pos_cats = [questions[i]["category"] for i,v in answers.items()
                        if v=="Yes" and i<len(questions)]
            if pos_cats:
                st.markdown(f"#### {t['pos_domains']}")
                tc = ["#f43f5e","#f59e0b","#a855f7","#3b82f6","#10b981","#ec4899"]
                tags = "".join(
                    f"<span class='cat-tag' style='background:{tc[i%6]}18;"
                    f"border:1px solid {tc[i%6]}44;color:{tc[i%6]};'>● {cat}</span>"
                    for i,cat in enumerate(pos_cats)
                )
                st.markdown(f"<div style='margin-bottom:1rem;display:flex;flex-wrap:wrap;gap:.4rem;'>{tags}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"""<div style='background:#022c22;border:1px solid #10b981;
                    border-radius:12px;padding:.9rem 1.2rem;color:#10b981;
                    font-size:.9rem;margin-bottom:1rem;'>{t['no_positive']}</div>""",
                    unsafe_allow_html=True)

            # Answer summary
            st.markdown(f"#### {t['summary']}")
            rows = ""
            for i,q in enumerate(questions):
                ans = answers.get(i,"—")
                ac  = "#f43f5e" if ans=="Yes" else ("#10b981" if ans=="No" else "#64748b")
                ab  = "#f43f5e11" if ans=="Yes" else ("#10b98111" if ans=="No" else "transparent")
                rows += (f"<div class='result-row'>"
                         f"<span class='r-qnum'>Q{i+1}</span>"
                         f"<span class='r-text'>{q['text']}</span>"
                         f"<span class='r-ans' style='color:{ac};background:{ab};"
                         f"border-radius:6px;padding:.15rem .5rem;'>{ans}</span></div>")
            st.markdown(f"<div class='bat-card' style='padding:1.2rem 1.5rem;'>{rows}</div>",
                        unsafe_allow_html=True)

            # Disclaimer
            st.markdown(f"<div class='disclaimer'>{t['disclaimer']}</div>",
                        unsafe_allow_html=True)

            st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

            # ── PDF DOWNLOAD ─────────────────────────────────────────────────
            st.markdown(f"#### {t['download_pdf']}")
            with st.spinner(t["pdf_generating"]):
                chart_buf.seek(0)
                pdf_buf = build_pdf(patient, questions, answers,
                                    yes_count, total_ans, weighted, result, t, chart_buf)
            safe_name = st.session_state.pt_name.replace(" ","_") or "patient"
            st.download_button(
                label=t["download_pdf"],
                data=pdf_buf,
                file_name=f"BAT_Report_{safe_name}_{st.session_state.pt_date}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )

            st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
            b1,b2 = st.columns(2)
            with b1:
                if st.button(t["retake"], use_container_width=True, type="primary"):
                    for k in ["answers","gender","questions","pt_name","pt_age","pt_id"]:
                        st.session_state[k] = {} if k=="answers" else ([] if k=="questions" else (None if k=="gender" else ""))
                    st.session_state.pt_age = 0
                    go_to(0); st.rerun()
            with b2:
                if st.button(t["review"], use_container_width=True):
                    go_to(3); st.rerun()
