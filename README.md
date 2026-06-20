#  The Daily Ink

A minimalist, fully automated digital newspaper designed for E-Ink displays (specifically optimized for Raspberry Pi Zero with Pimoroni Inky displays). It fetches daily knowledge, news, weather, and a comic strip, rendering them into a clean, pixel-perfect, vintage newspaper layout.

With its new cloud-rendered architecture, all heavy processing is handled by GitHub Actions, allowing the Raspberry Pi to act as a highly efficient, lightweight client that simply wakes up, downloads the daily image, and updates the screen.

##  Features
* **Cloud Rendering Engine:** Uses GitHub Actions to fetch data and render the layout via headless Chromium, saving local hardware resources.
* **Modular Architecture:** Cleanly separated Python modules for easy expansion (Weather, Wiki, History, Tech News, Culture, etc.).
* **Decoupled Templates:** HTML/CSS layout is isolated from the logic for easy styling tweaks.
* **Hardware Optimized:** Automatically rotates and resizes images to natively fit Pimoroni Inky displays (480x800 resolution).
* **Automated Delivery:** Fully synced cronjobs ensure a fresh paper is waiting for you every morning at 5:00 AM.

---

##  Project Structure

```text
the-daily-ink/
├── modules/
│   ├── __init__.py
│   ├── weather.py         # OpenWeatherMap API
│   ├── news.py            # Wiki, Verge RSS, History API
│   └── culture.py         # Useless facts, Wordnik, Quotes, XKCD
├── templates/
│   └── layout.html        # HTML/CSS structural template
├── generate.py            # Main cloud orchestration script
├── requirements.txt       # Python dependencies
└── .github/workflows/
    └── main.yml           # GitHub Actions automation schedule

 Quick Start (Local Testing)
If you want to run or test the generator on your local PC:
1. Clone the repository:

Bash
git clone [https://github.com/PrymeTyme/the-daily-ink.git](https://github.com/PrymeTyme/the-daily-ink.git)
cd the-daily-ink
2. Create a virtual environment and install dependencies:
Bash

python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
3. Set up local environment variables: Create a .env file in the root directory and add your keys:
Plaintext

OPENWEATHER_API_KEY=your_api_key_here
WEATHER_CITY=Bregenz, AT

4. Generate a test newspaper:

Bash
python generate.py
(This will output a newspaper.png file in your directory).
 GitHub Actions Setup (Server)
To automate the daily generation in the cloud:

1.	Go to your GitHub Repository Settings -> Secrets and variables -> Actions.
2.	Secrets Tab: Add a new secret named OPENWEATHER_API_KEY with your OpenWeatherMap API key.
3.	Variables Tab: Add a new variable named WEATHER_CITY with your target location (e.g., Bregenz, AT - do not use quotes).
4.	The GitHub Action will automatically run every day at 03:00 UTC (05:00 AM local summer time) and commit the fresh newspaper.png directly to the main branch.

 Raspberry Pi Zero Setup (Client)
The Pi simply wakes up, grabs the image from GitHub, and pushes it to the Inky display.

1. SSH into your Raspberry Pi and edit your crontab:
Bash
crontab -e
2. Add the daily cronjob: (This runs at 5:15 AM local time, uses the pimoroni virtual environment, and logs output to cron.log)
Bash

15 5 * * * /home/admin/.virtualenvs/pimoroni/bin/python /home/admin/newspaper_client/update_display.py >> /home/admin/newspaper_client/cron.log 2>&1

 Disclaimer & Copyright
This project acts purely as an aggregator for personal, non-commercial use.
•	XKCD Comics: Comic strips are fetched from xkcd.com and are licensed under the Creative Commons Attribution-NonCommercial 2.5 License.
•	News & APIs: All news headlines, historical facts, and weather data belong to their respective creators and APIs (e.g., Wikipedia, The Verge, OpenWeatherMap, Wordnik, ZenQuotes, Muffinlabs History API).

Please ensure you comply with the terms of service of the respective APIs if you modify the fetch requests.
