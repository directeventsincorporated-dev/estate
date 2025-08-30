# estate

This repository contains a small Python script that reports:

- Local time and day based on your IP address
- Current weather at your location
- Traffic information (requires a TomTom API key)

## Requirements

The script uses only Python's standard library but requires internet access.

For traffic data you must provide a TomTom API key via the `TOMTOM_API_KEY` environment variable.

## Usage

```bash
python app.py
```

If `TOMTOM_API_KEY` is set, traffic speed information will also be displayed.
