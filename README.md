E-WASTE CLASSIFICATION — QUICK START (WINDOWS)
================================================

WHAT THIS PROJECT DOES
- Lets you upload a photo of discarded electronic equipment.
- With Gemini enabled, AI predicts one of eight e-waste categories.
- Shows a confidence estimate, a short reason and a safe next step.
- Includes a demo mode so you can check that the app launches without an API key.

RUN IT
1. Extract the entire ZIP file to a normal folder, such as Desktop\EWasteClassifier.
2. Install Python 3.10 or newer from https://www.python.org/downloads/
   On Windows, enable "Add Python to PATH" during installation if shown.
3. Open the extracted folder.
4. Double-click START_EWASTE_CLASSIFIER.bat.
5. The first launch creates a virtual environment and installs packages.
   This needs internet and may take a few minutes.
6. Streamlit should open in your browser. If not, open http://localhost:8501.

ENABLE REAL IMAGE CLASSIFICATION
1. Visit https://aistudio.google.com/app/apikey
2. Create a Gemini API key.
3. In the app's left sidebar, paste the key into "Gemini API key".
4. Upload a clear photo and click "Classify E-Waste".
The key is entered in the running app session. Do not share it or upload it to GitHub.
Google's model availability, usage limits and billing terms can change; check AI Studio.

DEMO MODE
Without an API key, the app opens and lets you test the interface, but it does NOT
analyse the image. It clearly labels the output as demo mode. Real image classification
requires the Gemini API key and an internet connection.

SUPPORTED CATEGORIES
- Battery
- Mobile phone / tablet
- Computer / laptop
- Cable / wire
- Circuit board / electronic component
- Monitor / television
- Printer / scanner
- Other electronic waste

TROUBLESHOOTING
- Python not recognized: install Python and enable Add Python to PATH.
- Browser did not open: visit http://localhost:8501 manually.
- Install failed: check internet and run the BAT file again.
- AI failed: check API key, internet, model availability and AI Studio limits.
- Stop app: focus the command window and press Ctrl+C.

SAFETY
Do not dismantle, burn, crush or puncture e-waste. Do not handle swollen, leaking or
damaged batteries. Keep them away from heat and contact an authorised collection
or recycling facility. AI predictions are estimates, not official waste determinations.
Always follow local disposal rules.
