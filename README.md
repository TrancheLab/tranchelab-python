# tranchelab-python

Python client for the [TrancheLab](https://tranchelab.com) API.

TrancheLab extracts structured capital structures from Chapter 11 bankruptcy disclosure statements in minutes, with source citations and confidence scores on every value.

## Installation

```bash
pip install tranchelab
```

## Quick Start

```python
from tranchelab import TrancheLab

client = TrancheLab(api_key="your-api-key")

extraction = client.extract("hertz-disclosure-statement.pdf", case_number="20-11218")

print(extraction.debtor)
# → The Hertz Corporation

print(extraction.extraction_confidence)
# → 0.69

for tranche in extraction.capital_structure.secured_debt:
    print(f"{tranche.tranche}: {tranche.amount} (page {tranche.source_page})")
# → First Lien Term Loan: $656,000,000 (page 39)
# → First Lien Revolving Credit Facility: $615,000,000 (page 39)
# → ...
```

## Authentication

Set your API key as an environment variable:

```bash
export TRANCHELAB_API_KEY=your-api-key
```

Or pass it directly:

```python
client = TrancheLab(api_key="your-api-key")
```

## Methods

### `client.extract(file_path, case_number=None)`
Submit a PDF for extraction. Returns an `Extraction` object.

### `client.get_extraction(extraction_id)`
Retrieve a previously completed extraction by ID.

### `client.list_extractions(limit=20, offset=0)`
List all extractions for your account.

## Output Schema

Every extraction returns a structured `Extraction` object:

```python
extraction.case_number          # "20-11218"
extraction.debtor               # "The Hertz Corporation"
extraction.court                # "U.S. Bankruptcy Court, District of Delaware"
extraction.extraction_confidence  # 0.69
extraction.validation_flags     # ["APR_CONFLICT"]
extraction.rsa_detected         # True

# Capital structure — grouped by category
extraction.capital_structure.dip_financing    # List[Tranche]
extraction.capital_structure.secured_debt     # List[Tranche]
extraction.capital_structure.unsecured_debt   # List[Tranche]
extraction.capital_structure.exit_financing   # List[Tranche]
extraction.capital_structure.equity           # List[Tranche]

# Each Tranche has:
tranche.tranche          # "First Lien Term Loan"
tranche.amount           # "$656,000,000"
tranche.amount_normalized  # 656000000
tranche.confidence       # 0.75
tranche.source_page      # 39
tranche.source_text      # "First Lien Term Loan $656 million"
```

See the full schema at [TrancheLab/extraction-schema](https://github.com/TrancheLab/extraction-schema).

## API Access

The TrancheLab API is currently invite-only.
Request access at [tranchelab.com](https://tranchelab.com).

## License

MIT
