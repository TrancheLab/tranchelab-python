from tranchelab import TrancheLab

client = TrancheLab(api_key="your-api-key")

# Extract a disclosure statement PDF
extraction = client.extract(
    file_path="hertz-disclosure-statement.pdf",
    case_number="20-11218"
)

print(f"Debtor: {extraction.debtor}")
print(f"Court: {extraction.court}")
print(f"Confidence: {extraction.extraction_confidence:.2f}")
print(f"Flags: {extraction.validation_flags}")
print()

# Print secured debt tranches
print("Secured Debt:")
for tranche in extraction.capital_structure.secured_debt:
    print(f"  {tranche.tranche}: {tranche.amount} (conf: {tranche.confidence}, pg: {tranche.source_page})")

print()
print("Unsecured Debt:")
for tranche in extraction.capital_structure.unsecured_debt:
    print(f"  {tranche.tranche}: {tranche.amount} (conf: {tranche.confidence}, pg: {tranche.source_page})")
