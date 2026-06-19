# The Daily Ink 

A minimalist, modular, daily digital newspaper designed for E-Ink displays (like Raspberry Pi Zero with Pimoroni Inky displays). It fetches daily knowledge, news, weather, and a comic strip, rendering them into a clean, pixel-perfect, vintage newspaper layout.

## Features
* **Modular Design:** Easily add or remove modules (Weather, Wiki, History, Tech News, etc.).
* **Pixel-Perfect Layout:** Uses CSS Flexbox for strict column alignment on a 480x800 resolution.
* **Lightweight:** Designed to run efficiently on low-resource hardware like the Raspberry Pi Zero.

## Quick Start

1. Clone the repository:
   ``
   git clone [https://github.com/YOUR_USERNAME/the-daily-ink.git](https://github.com/YOUR_USERNAME/the-daily-ink.git) ´´
   cd the-daily-ink

2. Install dependencies:
    

    pip install -r requirements.txt

3.  Set up environment variables:
    Copy .env.example to .env and add your API keys (e.g., OpenWeatherMap).

4.  Run the generator:
    

    python app.py

Disclaimer & Copyright

This project acts purely as an aggregator for personal, non-commercial use.

    XKCD Comics: Comic strips are fetched from xkcd.com and are licensed under the Creative Commons Attribution-NonCommercial 2.5 License.

    News & APIs: All news headlines, historical facts, and weather data belong to their respective creators and APIs (e.g., Wikipedia, The Verge, OpenWeatherMap, Muffinlabs History API).

Please ensure you comply with the terms of service of the respective APIs if you modify the fetch requests.   