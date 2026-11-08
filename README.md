# RA On-Shift Helper

**natHacks 2026 Submission – Defense & Security (Infrastructure & Operational Security)**

RA On-Shift Helper is a lightweight, mobile-responsive web application designed to bridge the gap between student residence incident reporting and Residence Assistant (RA) shift handoffs. It provides students with a confidential way to report maintenance, noise, and safety hazards, while giving RAs an interactive, geospatial dashboard to triage hotspots during their rounds.

## The Problem
Residence safety and maintenance relies heavily on fragmented communication. Students hesitate to report issues due to privacy concerns or clunky web portals, and RAs starting their shifts often inherit a disorganized list of overnight logs without a clear understanding of spatial hotspots (e.g., a clustered pattern of propped doors in a specific stairwell).

## The Solution
*   📱 **Student Mobile Interface:** A streamlined, mobile-friendly reporting tool that allows students to document incidents, tag specific building zones, and drop custom location pins via an interactive map.

*   🗺️ **Interactive Patrol Map:** RAs access a live dashboard with an OpenStreetMap overlay (powered by Folium) that clusters incidents over the exact footprints of the residence towers, color-coded by urgency.
*   📊 **Shift Handoff Dashboard:** Visualizes incident hotspots by zone and allows RAs to filter by building or status, ensuring a clean transition between shifts.

## Tech Stack
*   **Frontend & Framework:** Streamlit (Python)
*   **Mapping & Geospatial:** Folium, `streamlit-folium`
*   **Data Processing & Storage:** Pandas, Regex (Local CSV storage for hackathon prototype)

## Project Structure
*   `app.py` — The main Streamlit application containing the UI rendering and map logic.
*   `privacy_triage.py` — The local text-processing engine that categorizes urgency and scrubs PII.
*   `storage.py` — Handles reading, saving, and updating incident records.
*   `incidents.csv` — The local database (pre-populated with 43 simulated overnight incidents for demonstration).
*   `requirements.txt` — Required Python dependencies.

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Install the dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application RA:**
   ```bash
   streamlit run ra_app.py
   ```
4. **Start the application as student:**
   ```bash
   streamlit run student_app.py
   ```
5. **Test the app:**
   *   The app will automatically open in your browser at `http://localhost:8501`.
   *   Use the sidebar to toggle between the **Student Report (Phone)** view and the **RA Dashboard** view.