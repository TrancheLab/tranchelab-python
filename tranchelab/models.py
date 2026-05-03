from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Tranche:
    tranche: str
    amount: str
    amount_normalized: Optional[int]
    priority: int
    confidence: float
    source_page: int
    source_text: str
    lender: Optional[str] = None
    source_section: Optional[str] = None
    recovery_estimate: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Tranche":
        return cls(
            tranche=data["tranche"],
            amount=data["amount"],
            amount_normalized=data.get("amount_normalized"),
            priority=data["priority"],
            confidence=data["confidence"],
            source_page=data["source_page"],
            source_text=data["source_text"],
            lender=data.get("lender"),
            source_section=data.get("source_section"),
            recovery_estimate=data.get("recovery_estimate"),
        )


@dataclass
class CapitalStructure:
    dip_financing: List[Tranche] = field(default_factory=list)
    secured_debt: List[Tranche] = field(default_factory=list)
    unsecured_debt: List[Tranche] = field(default_factory=list)
    vehicle_financing: List[Tranche] = field(default_factory=list)
    exit_financing: List[Tranche] = field(default_factory=list)
    equity: List[Tranche] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "CapitalStructure":
        def parse_tranches(key):
            return [Tranche.from_dict(t) for t in data.get(key, [])]

        return cls(
            dip_financing=parse_tranches("dip_financing"),
            secured_debt=parse_tranches("secured_debt"),
            unsecured_debt=parse_tranches("unsecured_debt"),
            vehicle_financing=parse_tranches("vehicle_financing"),
            exit_financing=parse_tranches("exit_financing"),
            equity=parse_tranches("equity"),
        )

    @property
    def all_tranches(self) -> List[Tranche]:
        return (
            self.dip_financing
            + self.secured_debt
            + self.unsecured_debt
            + self.vehicle_financing
            + self.exit_financing
            + self.equity
        )


@dataclass
class Extraction:
    case_number: str
    debtor: str
    court: str
    extracted_at: str
    extraction_confidence: float
    capital_structure: CapitalStructure
    filing_type: Optional[str] = None
    petition_date: Optional[str] = None
    document_pages: Optional[int] = None
    processing_time_seconds: Optional[float] = None
    validation_flags: List[str] = field(default_factory=list)
    rsa_detected: bool = False
    ica_detected: bool = False
    notes: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Extraction":
        return cls(
            case_number=data["case_number"],
            debtor=data["debtor"],
            court=data["court"],
            extracted_at=data["extracted_at"],
            extraction_confidence=data["extraction_confidence"],
            capital_structure=CapitalStructure.from_dict(data["capital_structure"]),
            filing_type=data.get("filing_type"),
            petition_date=data.get("petition_date"),
            document_pages=data.get("document_pages"),
            processing_time_seconds=data.get("processing_time_seconds"),
            validation_flags=data.get("validation_flags", []),
            rsa_detected=data.get("rsa_detected", False),
            ica_detected=data.get("ica_detected", False),
            notes=data.get("notes"),
        )
