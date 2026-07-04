### local_tumor_status
| Field | Type / allowed values |
| --- | --- |
| `morphology` | `"polypoid"`, `"semi-annular"`, `"annular"`, `"missing"` |
| `mucinous_component` | `"yes"`, `"no"`, `"missing"` |
| `circumferential_tumor_involvement_start` | Integer from `1` to `12`, or `null` |
| `circumferential_tumor_involvement_end` | Integer from `1` to `12`, or `null` |
| `rectal_tumor_location_in_rectum` | `"low"`, `"mid"`, `"high"` |
| `distance_from_anorectal_junction_to_distal_tumor_border_cm` | Number in centimetres, or `null` |
| `relation_to_anterior_peritoneal_reflection` | `"below"`, `"at the level of"`, `"above"`, `"missing"` |
| `tumor_length_cm` | Number in centimetres, or `null` |
| `t_stage` | `"T1_2"`, `"T3a"`, `"T3b"`, `"T3c"`, `"T3d"`, `"T4a"`, `"T4b"`, `"missing"` |
| `invaded_structures` | String; empty when not applicable, or `"missing"` |
| `sphincter_complex_invasion` | `"no"`, `"yes, internal sphincter only"`, `"yes, internal sphincter + intersphincteric plane"`, `"yes, internal + external sphincter"`, `"missing"` |
| `lowest_part_of_sphincter_invasion` | `"upper"`, `"middle"`, `"distal"`, `"not applicable"`, `"missing"` |

### mesorectal_fascia_involement
| Field | Type / allowed values |
| --- | --- |
| `margin` | `"clear(> 1 mm)"`, `"involved(<= 1 mm)"`, `"missing"` |
| `circumferential_location_of_shortest_distance` | Integer from `1` to `12`, or `null` |
| `involved_by` | `"tumor"`, `"EMVI"`, `"tumor deposit"`, `"not applicable"`, `"missing"` |

### lymph_nodes_and_tumor_deposits
| Field | Type / allowed values |
| --- | --- |
| `regional_total_suspicious_mesorectal_nodes` | Non-negative integer, or `null` |
| `nodes_short_axis_ge_9mm` | Non-negative integer, or `null` |
| `nodes_from_5_to_8mm_with_2_morphologic_criteria` | Non-negative integer, or `null` |
| `nodes_5mm_with_all_3_morphologic_criteria` | Non-negative integer, or `null` |
| `mucinous_nodes_any_size` | Non-negative integer, or `null` |
| `regional_total_suspicious_extramesorectal_nodes` | Non-negative integer, or `null` |
| `n_stage` | `"N0"`, `"N1"`, `"N2"`, `"missing"` |
| `tumor_deposits_within_mesorectum` | Non-negative integer, or `null` |

### emvi
| Field | Type / allowed values |
| --- | --- |
| `presence_of_emvi` | `"yes"`, `"no"`, `"missing"` |
| `emvi_clock_position` | Integer from `1` to `12`, or `null` |
