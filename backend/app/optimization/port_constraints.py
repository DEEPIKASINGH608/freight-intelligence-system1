"""
Port constraints validator for SIH26006 specification.
Validates vessel draft, LOA, beam, DWT, and cargo handling compatibility.
"""

PORT_CONSTRAINTS = {
    "Paradip": {
        "max_draft_m": 17.0,
        "max_loa_m": 300.0,
        "max_beam_m": 48.0,
        "supported_cargos": ["iron_ore", "coal", "bauxite"],
        "max_dwt": 180000
    },
    "Vizag": {
        "max_draft_m": 16.5,
        "max_loa_m": 280.0,
        "max_beam_m": 45.0,
        "supported_cargos": ["iron_ore", "coal"],
        "max_dwt": 150000
    },
    "Gangavaram": {
        "max_draft_m": 18.1,
        "max_loa_m": 310.0,
        "max_beam_m": 50.0,
        "supported_cargos": ["iron_ore", "coal", "limestone"],
        "max_dwt": 200000
    }
}


def validate_vessel_port_compatibility(
    vessel: dict,
    port_name: str,
    cargo_type: str = "iron_ore"
) -> tuple[bool, list[str]]:
    """
    Checks if a vessel can call at the specified port given physical constraints.
    Returns (is_compatible, list_of_violations).
    """
    violations = []
    port = PORT_CONSTRAINTS.get(port_name)

    if not port:
        # Default pass if port is not in database, but allow fallback execution
        return True, []

    draft = vessel.get("draft_m", 0)
    loa = vessel.get("loa_m", 0)
    beam = vessel.get("beam_m", 0)
    dwt = vessel.get("capacity_dwt", 0)

    if draft > port["max_draft_m"]:
        violations.append(
            f"Vessel draft ({draft}m) exceeds port max draft ({port['max_draft_m']}m)"
        )

    if loa > port["max_loa_m"]:
        violations.append(
            f"Vessel LOA ({loa}m) exceeds port max LOA ({port['max_loa_m']}m)"
        )

    if beam > port["max_beam_m"]:
        violations.append(
            f"Vessel beam ({beam}m) exceeds port max beam ({port['max_beam_m']}m)"
        )

    if cargo_type not in port["supported_cargos"]:
        violations.append(
            f"Cargo type '{cargo_type}' is not supported at {port_name} port"
        )

    if dwt > port["max_dwt"]:
        violations.append(
            f"Vessel DWT ({dwt} MT) exceeds port max capacity ({port['max_dwt']} MT)"
        )

    is_compatible = len(violations) == 0
    return is_compatible, violations