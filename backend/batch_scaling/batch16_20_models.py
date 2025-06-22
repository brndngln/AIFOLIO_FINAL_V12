from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import datetime

# --- Batch 16 Models ---
class MultiCurrencyRevenue(BaseModel):
    currency: str
    amount: float
    date: datetime.date

class TaxRegionReport(BaseModel):
    region: str
    compliance_status: str
    last_reviewed: datetime.date

class VaultLicenseMap(BaseModel):
    country: str
    license_status: str
    notes: Optional[str]

class ComplianceStatus(BaseModel):
    region: str
    status: str
    details: Optional[str]

class PartnerAPILegalHealth(BaseModel):
    partner: str
    status: str
    notes: Optional[str]

class VaultEcosystemScore(BaseModel):
    region: str
    maturity_score: int
    notes: Optional[str]

# --- Batch 17 Models ---
class ExecutiveSummary(BaseModel):
    year: int
    summary: str

class CEOReport(BaseModel):
    year: int
    highlights: str

class BusinessImpactMap(BaseModel):
    region: str
    impact_score: int
    notes: Optional[str]

class LegalTerm(BaseModel):
    partner: str
    terms: str
    valid_until: datetime.date

class ESGScore(BaseModel):
    region: str
    score: int
    notes: Optional[str]

class IPOverlapMap(BaseModel):
    vaults: List[str]
    overlap_notes: str

# --- Batch 18 Models ---
class ResilienceAudit(BaseModel):
    year: int
    findings: str

class AlignmentReport(BaseModel):
    partners: List[str]
    alignment_score: int
    notes: Optional[str]

class GovernanceBoardReport(BaseModel):
    year: int
    summary: str

class MultiYearCompliance(BaseModel):
    year: int
    status: str
    notes: Optional[str]

class AuditorCertification(BaseModel):
    auditor: str
    year: int
    certified: bool
    notes: Optional[str]

class RoadmapSummary(BaseModel):
    year: int
    summary: str

# --- Partner Certification System ---
class PartnerCertification(BaseModel):
    partner: str
    certified: bool
    last_audit: datetime.date
    notes: Optional[str]

class PartnerSelfCertSubmission(BaseModel):
    partner: str
    submission_date: datetime.date
    details: str

class CertificationAuditReport(BaseModel):
    partner: str
    year: int
    findings: str

# --- Batch 19 Models ---
class Web3LegalCompatibility(BaseModel):
    chain: str
    compatible: bool
    notes: Optional[str]

class CrossChainRevenue(BaseModel):
    chain: str
    revenue: float
    date: datetime.date

class NFTLicensing(BaseModel):
    nft_id: str
    licensed: bool
    notes: Optional[str]

class Web3PartnerAudit(BaseModel):
    partner: str
    findings: str
    date: datetime.date

class BlockchainTransparency(BaseModel):
    chain: str
    transparency_score: int
    notes: Optional[str]

class DigitalAssetIPRisk(BaseModel):
    asset: str
    risk_level: str
    notes: Optional[str]

# --- Batch 20 Models ---
class EnterpriseMaturityIndex(BaseModel):
    enterprise: str
    maturity_score: int
    notes: Optional[str]

class FutureTrendsTracker(BaseModel):
    year: int
    trends: str

class PolicyCrossCheck(BaseModel):
    policy: str
    status: str
    notes: Optional[str]

class PartnerNetworkHealth(BaseModel):
    partner: str
    health_score: int
    notes: Optional[str]

class SystemRenewalPlan(BaseModel):
    year: int
    plan: str

class TrustedPartnerReport(BaseModel):
    partner: str
    year: int
    public_report: str
