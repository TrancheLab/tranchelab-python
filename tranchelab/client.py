import os
import requests
from typing import Optional, List
from .models import Extraction
from .exceptions import AuthenticationError, ExtractionError, NotFoundError, TranceLabError

BASE_URL = "https://api.tranchelab.com/v1"


class TrancheLab:
    """
    Python client for the TrancheLab API.

    Usage:
        from tranchelab import TrancheLab

        client = TrancheLab(api_key="your-api-key")
        extraction = client.extract("path/to/disclosure.pdf")
        print(extraction.debtor)
        print(extraction.capital_structure.secured_debt)
    """

    def __init__(self, api_key: Optional[str] = None, base_url: str = BASE_URL):
        self.api_key = api_key or os.environ.get("TRANCHELAB_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "No API key provided. Pass api_key= or set the TRANCHELAB_API_KEY environment variable."
            )
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "tranchelab-python/0.1.0",
        })

    def _request(self, method: str, path: str, **kwargs) -> dict:
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, **kwargs)

        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired API key.", status_code=401)
        if response.status_code == 404:
            raise NotFoundError("Resource not found.", status_code=404)
        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            raise TranceLabError(f"API error: {detail}", status_code=response.status_code)

        return response.json()

    def extract(self, file_path: str, case_number: Optional[str] = None) -> Extraction:
        """
        Submit a PDF for extraction and return the structured capital structure.

        Args:
            file_path: Path to the PDF file to extract.
            case_number: Optional PACER case number for metadata association.

        Returns:
            Extraction object with full capital structure.
        """
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f, "application/pdf")}
            data = {}
            if case_number:
                data["case_number"] = case_number

            response = self.session.post(
                f"{self.base_url}/extract",
                files=files,
                data=data,
            )

        if response.status_code == 401:
            raise AuthenticationError("Invalid or expired API key.", status_code=401)
        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            raise ExtractionError(f"Extraction failed: {detail}", status_code=response.status_code)

        return Extraction.from_dict(response.json())

    def get_extraction(self, extraction_id: str) -> Extraction:
        """
        Retrieve a previously completed extraction by ID.

        Args:
            extraction_id: The extraction ID returned from extract().

        Returns:
            Extraction object.
        """
        data = self._request("GET", f"/extractions/{extraction_id}")
        return Extraction.from_dict(data)

    def list_extractions(self, limit: int = 20, offset: int = 0) -> List[Extraction]:
        """
        List all extractions for your account.

        Args:
            limit: Number of results to return (default 20, max 100).
            offset: Pagination offset.

        Returns:
            List of Extraction objects.
        """
        data = self._request("GET", f"/extractions", params={"limit": limit, "offset": offset})
        return [Extraction.from_dict(e) for e in data.get("extractions", [])]
