from tranchelab import TrancheLab

client = TrancheLab(api_key="your-api-key")

extractions = client.list_extractions(limit=10)

for e in extractions:
    print(f"{e.case_number} — {e.debtor} — confidence: {e.extraction_confidence:.2f}")
