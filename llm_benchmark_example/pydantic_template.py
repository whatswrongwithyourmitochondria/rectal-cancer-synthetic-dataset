from typing import Optional, Literal
from pydantic import BaseModel, Field

class LocalTumorStatus(BaseModel):
    morphology: Literal["polypoid", "semi-annular", "annular", "missing"] = Field(
        default="missing",
        alias='Morphology: [Polypoid/(semi-)annular]'
    )
    mucinous_component: Literal["yes", "no", "missing"] = Field(
        default="missing",
        alias='Mucinous component: [yes/no]'
    )
    circumferential_tumor_involvement_start: Optional[int] = Field(
        ...,
        alias='Circumferential tumour involvement: from [ ] o clock'
    )
    circumferential_tumor_involvement_end: Optional[int] = Field(
        ...,
        alias='Circumferential tumour involvement: to [ ] o clock'
    )
    rectal_tumor_location_in_rectum: Literal["low", "mid", "high"] = Field(
        default="mid",
        alias='[low/mid/high] rectal tumour'
    )
    distance_from_anorectal_junction_to_distal_tumor_border_cm: Optional[float] = Field(
        ...,
        alias='Distance from anorectal junction to distal tumour border: [ ] cm'
    )
    relation_to_anterior_peritoneal_reflection: Literal["below", "at the level of", "above", "missing"] = Field(
        default="missing",
        alias='Relation to anterior peritoneal reflection: [below/at the level of/above]'
    )
    tumor_length_cm: Optional[float] = Field(
        ...,
        alias='Tumour length: [ ] cm'
    )
    t_stage: Literal["T1_2", "T3a", "T3b", "T3c", "T3d", "T4a", "T4b", "missing"] = Field(
        default="missing",
        alias='T-stage: [T1-2/T3a/T3b/T3c/T3d/T4a/T4b]'
    )
    invaded_structures: Optional[str] = Field(
        default="",
        alias='If T4b, structures with possible invasion: [ ]'
    )
    sphincter_complex_invasion: Literal["no", "yes, internal sphincter only", "yes, internal sphincter and intersphincteric plane", "yes, internal sphincter and intersphincteric plane and external sphincter", "missing"] = Field(
        default="no",
        alias='Anal sphincter complex invasion: [No/Involves internal sphincter only/+ intersphincteric plane/+ external sphincter]'
    )
    lowest_part_of_sphincter_invasion: Literal["upper", "middle", "distal", "not applicable", "missing"] = Field(
        default="not applicable",
        alias='If yes, lowest part of invasion [upper/middle/distal] third of anal canal'
    )


class MesorectalFasciaInvolement(BaseModel):
    margin: Literal["clear(> 1 mm)", "involved(<= 1 mm)", "missing"] = Field(
        default="missing",
        alias='Mesorectal fascia (MRF) involvement: [clear(> 1 mm)/involved(≤ 1 mm)]'
    )
    circumferential_location_of_shortest_distance: Optional[int] = Field(...,
        alias='If involved: at [ ] o clock' # Alias refers to shortest distance between MRF and tumor/tumor deposit/EMVI
    )
    involved_by: Literal["tumour", "EMVI", "tumor deposit", "missing", "not applicable"] = Field(
        default="not applicable",
        alias='by [tumour/EMVI/tumour deposit]'
    )


class LymphNodesAndTumourDeposits(BaseModel):
    regional_total_suspicious_mesorectal_nodes: Optional[int] = Field(
        ...,
        alias='Total number of suspicious mesorectal lymph nodes : [ ]'
    )
    nodes_short_axis_ge_9mm: Optional[int] = Field(
        alias='[ ] nodes with short axis ≥ 9 mm'
    )
    nodes_from_5_to_8mm_with_2_morphologic_criteria: Optional[int] = Field(
        alias='[ ] nodes with short axis 5–8 mm and at least 2 morphologic suspicious criteria'
    )
    nodes_5mm_with_all_3_morphologic_criteria: Optional[int] = Field(
        alias='[ ] nodes with short axis 5 mm and all 3 morphologic suspicious criteria'
    )
    mucinous_nodes_any_size: Optional[int] = Field(
        alias='[ ] mucinous nodes (any size)'
    )
    regional_total_suspicious_extramesorectal_nodes: Optional[int] = Field(
        ...,
        alias='Total number of suspicious extramesorectal lymph nodes : [ ]'
    )
    n_stage: Literal["N0", "N1", "N2", "missing"] = Field(
        default="missing",
        alias='N-stage: [N0/N1/N2]'
    )
    tumor_deposits_within_mesorectum: Optional[int] = Field(
        ...,
        alias='Number of tumour deposits within the mesorectum: [ ]'
    )


class ExtramuralVascularInvasion(BaseModel):
    presence_of_emvi: Literal["yes", "no", "missing"] = Field(
        default="missing",
        alias='Presence of EMVI: [yes/no]'
    )
    emvi_clock_position: Optional[int] = Field(...,
        alias='If positive: at [ ] o clock'
    )


class RectalCancerReport(BaseModel):
    local_tumor_status: LocalTumorStatus = Field(
        ...,
        alias='Local tumour status'
    )
    mesorectal_fascia_involement: MesorectalFasciaInvolement = Field(
        ...,
        alias='Mesorectal fascia (MRF) involvement'
    )
    lymph_nodes_and_tumor_deposits: LymphNodesAndTumourDeposits = Field(
        ...,
        alias='Lymph nodes and tumour deposits'
    )
    emvi: ExtramuralVascularInvasion = Field(
        ...,
        alias='Extramural vascular invasion (EMVI)'
    )
