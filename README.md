#  The Daily Ink

A minimalist, fully automated digital newspaper designed for E-Ink displays. It fetches daily knowledge, news, weather, and a comic strip, rendering them into a clean, pixel-perfect, vintage newspaper layout.

With its cloud-rendered architecture, all heavy processing is handled by GitHub Actions. This allows the display hardware to act as a highly efficient, lightweight client that simply wakes up, downloads the daily image, and updates the screen.

---

##  Hardware Used
To replicate the exact physical build of this project, you will need:
* **Raspberry Pi Zero W** (or Pi Zero 2 W) with headers soldered.
* **Pimoroni Inky Impression 7.3"** (7-colour e-paper display).
* A MicroSD card and a 5V power supply.

---

##  How to "Subscribe" (Make it your own!)

You don't need a server to run this. You can "subscribe" to your own personalized daily newspaper by forking this repository and letting GitHub Actions do the heavy lifting for free.

**1. Fork the Repository:**
Click the **Fork** button at the top right of this repository to copy it to your own GitHub account.

**2. Configure Your Location & APIs:**
Go to your forked repository's **Settings** -> **Secrets and variables** -> **Actions**.
* **Secrets Tab:** Add a new secret named `OPENWEATHER_API_KEY` and paste your free OpenWeatherMap API key.
* **Variables Tab:** Add a new variable named `WEATHER_CITY` and type your city (e.g., `Bregenz, AT` - *do not use quotes*).

**3. Enable GitHub Actions:**
Go to the **Actions** tab in your repository and click **"I understand my workflows, go ahead and enable them."** The Action will automatically generate a fresh `newspaper.png` every day at 03:00 UTC (5:00 AM local summer time) and commit it to your `main` branch.

**4. Update the Client Link:**
In your `pi_client/update_display.py` file, change the `IMAGE_URL` to match your new GitHub username:
`https://raw.githubusercontent.com/YOUR_USERNAME/the-daily-ink/main/newspaper.png`

---

##  Raspberry Pi Zero Setup (Client)

The Pi acts as a terminal. It wakes up, grabs the generated image from GitHub, pushes it to the Inky display, and goes back to sleep.

**1. Install the Pimoroni Software:**
Before running the client code, you must install the official Pimoroni drivers and enable the SPI interface. Follow the official guide here:
[Getting Started with Inky Impression - Installing the Software](https://learn.pimoroni.com/article/getting-started-with-inky-impression#installing-the-software)

**2. Setup the Client Directory:**
SSH into your Raspberry Pi and copy the `pi_client` folder from this repository.
```bash
# Navigate to the client folder
cd pi_client

# The Pimoroni installer creates a virtual environment called 'pimoroni'.
# Ensure your dependencies are installed there:
/home/admin/.virtualenvs/pimoroni/bin/pip install -r requirements-pi.txt
```

**3. Automate the Morning Delivery (Cronjob):**
Set the Pi to automatically update shortly after GitHub finishes generating the image.
```bash
crontab -e
```
Add this line to run the update every morning at 5:15 AM:
```bash
15 5 * * * /home/admin/.virtualenvs/pimoroni/bin/python /home/admin/pi_client/update_display.py >> /home/admin/pi_client/cron.log 2>&1
```

---

##  Local Testing & Modification

If you want to modify the Python generation logic or tweak the HTML layout on your local PC:

**1. Clone your fork and install dependencies:**
```bash
git clone [https://github.com/YOUR_USERNAME/the-daily-ink.git](https://github.com/YOUR_USERNAME/the-daily-ink.git)
cd the-daily-ink

python -m venv venv
# On Windows: .\venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
```

**2. Set local environment variables:** Create a `.env` file in the root directory:
```text
OPENWEATHER_API_KEY=your_api_key_here
WEATHER_CITY=Bregenz, AT
```

**3. Test the generator:**
```bash
python generate.py
```

---

##  Project Structure

```text
the-daily-ink/
├── modules/
│   ├── __init__.py
│   ├── weather.py         # OpenWeatherMap API
│   ├── news.py            # Wiki, Verge RSS, History API
│   └── culture.py         # Useless facts, Wordnik, Quotes, XKCD
├── pi_client/
│   ├── update_display.py    # Hardware deployment script
│   └── requirements-pi.txt  # Lightweight Pi dependencies
├── templates/
│   └── layout.html        # HTML/CSS structural template
├── generate.py            # Main cloud orchestration script
├── requirements.txt       # Cloud/Local Python dependencies
└── .github/workflows/
    └── main.yml           # GitHub Actions automation schedule
```

---

##  Disclaimer & Copyright

This project acts purely as an aggregator for personal, non-commercial use.

* **XKCD Comics:** Comic strips are fetched from [xkcd.com](https://xkcd.com) and are licensed under the Creative Commons Attribution-NonCommercial 2.5 License.
* **News & APIs:** All news headlines, historical facts, and weather data belong to their respective creators and APIs (e.g., Wikipedia, The Verge, OpenWeatherMap, Wordnik, ZenQuotes, Muffinlabs History API).

Please ensure you comply with the terms of service of the respective APIs if you modify the fetch requests.