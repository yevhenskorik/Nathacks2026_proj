# RA On-Shift Helper 🛡️

**NatHacks 2026 Submission**  
An intelligent incident management and AI triage platform for university residences.

**GitHub Repository:** [https://github.com/yevhenskorik/RA-Onshift-Helper.git](https://github.com/yevhenskorik/RA-Onshift-Helper.git)

---

## 💡 The Concept
During community support shifts, Residence Assistants (RAs) face a chaotic influx of texts, calls, and walk-ups. Critical emergencies can easily get buried under routine maintenance requests. 

**RA On-Shift Helper** solves this by providing a two-sided platform:
1. **Frictionless Student Portal:** Residents can instantly report issues and drop exact map pins without creating an account.
2. **Secure RA Dashboard:** An AI triage engine (powered by Claude with a local Ollama fallback) analyzes incoming reports, assigns an urgency score (1-5), and flags potential distress like harassment or medical emergencies. This ensures life-safety incidents immediately jump to the top of the RA's queue.

## 🚀 How to Access the Software

### For Judges (Live Demo)
You can access the live, deployed version of our application here: 
* **Live App:** `https://ra-onshift.streamlit.app/`(https://ra-onshift.streamlit.app/)

To explore the RA Dashboard, please use our test credentials:
* **Username:** `radavid`
* **Password:** `demo123`

### Run Locally (For Developers)
To run this project on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yevhenskorik/RA-Onshift-Helper.git
   cd RA-Onshift-Helper
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Secrets:**
   Create a `.streamlit/secrets.toml` file in the root directory and add your API keys:
   ```toml
   SUPABASE_URL = "your_supabase_url"
   SUPABASE_KEY = "your_supabase_key"
   ANTHROPIC_API_KEY = "your_anthropic_api_key"
   RA_INVITE_CODE = "your_invite_code"
   ```
4. **Run the application:**
   ```bash
   streamlit run auth.py
   ```

## 👥 Credits
* **Yevhen** - Database Architecture, Git Workflows
* **Renee** - AI Triage Integration, Prompt Engineering
* **David** - UI/UX & Frontend Integration
* **Angel** - Testing & Demo Preparation
* **Shuoen** -Geospatial Mapping (Folium) & Location Data Pipeline


## 🔗 Links & Presentation Info
* **Devpost Submission:** https://ra-onshift.streamlit.app/
* **Pitch Presentation:** Delivered live in-person at NatHacks 2026.
* **Tech Stack:** Python, Streamlit, Supabase, Folium, Anthropic Claude, Ollama, Pandas.