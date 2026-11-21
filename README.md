
# commercial-re-scraper

Python script to scrape commercial property listings and broker phone numbers from paginated directories and export them to Excel-ready CSV files.

### Features

- Extracts property details from directory pages.
- Collects publicly listed broker contact information.
- Follows pagination links.
- Removes duplicate listings.
- Exports data to CSV.

### Setup

```bash
pip install -r requirements.txt


<!-- FINAL PORTFOLIO VERIFICATION START -->
## Final Portfolio Verification

**Project scope:** Commercial real estate listing extraction, pagination handling, duplicate detection, and CSV export.

**Repository file inspection:** Completed.

**Automated test status:** PASSED

**Repository:** https://github.com/razibleads10-design/commercial-re-scraper

This project uses demonstration data where applicable.
No live-data, production-scale, or performance claims are implied
unless separately demonstrated and verified.

<!-- FINAL PORTFOLIO VERIFICATION END -->

## Extended Automated Test Verification

Additional automated tests were added and executed successfully.

Coverage includes:
- Invalid property listing handling
- Relative URL resolution
- Alternative pagination link handling
- Maximum page limit
- Request failure handling
- Repeated pagination URL protection
- HTTP request exception handling

All existing and extended tests were executed locally using pytest.
These tests use controlled sample HTML and mocked requests; they do not claim live website compatibility.
