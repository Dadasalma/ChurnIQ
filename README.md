
# ChurnIQ Interactive Dashboard

This folder contains the real interactive Streamlit dashboard for ChurnIQ.

## Step 1 — Export data from Colab
Paste the code from `COLAB_EXPORT_CELL.txt` into a new Colab cell and run it.
Download:
- `churniq_predictions.csv`
- `metrics.json`

Place them here:
```text
data/churniq_predictions.csv
reports/metrics.json
```

## Step 2 — Run / deploy
Local command:
```bash
streamlit run app/dashboard.py
```

Because Windows Application Control blocks compiled Python extensions on the current PC,
the recommended final route is deployment through Streamlit Community Cloud after
uploading this project to GitHub.

## Dashboard sections
- Overview
- Risk Analytics
- Model & Drivers
- Customer Priorities
- Interactive filters
- Downloadable retention-priority CSV

Revenue-at-risk is an analytical estimate, not realized loss.
