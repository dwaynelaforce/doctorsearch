from urllib.parse import quote

import requests

from base_classes import (
    Doctor, 
    Results, 
    QueryStatus, 
    LicenseStatus, 
    MedicalLicense
)

URL = "https://data.wa.gov/resource/qxh8-f4bd.json"

def generate_soql(**kwargs: dict[str, str]) -> str:
    # $where=upper(`firstname`) LIKE 'KIN%' AND `credentialtype` = 'Physician And Surgeon License')
    arguments = [
        f"upper({k}) LIKE '{v.upper()}%'"
        for k, v in kwargs.items()
    ] + [
        "upper(credentialtype) like '%PHYSICIAN AND SURGEON%'",
    ]
    soql = " AND ".join(arguments)
    return soql

def license_search(doctor: Doctor) -> Results:
    print("Searching for: ", doctor)
    soql = generate_soql(lastname=doctor.lastname, firstname=doctor.firstname)
    url = f"{URL}?$where={quote(soql)}"
    json_results: dict | list = requests.get(url, timeout=30).json()

    if isinstance(json_results, dict):
        response = Results(QueryStatus.ERROR)
        if msg := json_results.get("message", ""):
            response.notes.append(msg)
        return response

    if not len(json_results):
        return Results(QueryStatus.NOT_FOUND)

    if len(json_results) > 1:
        notes = [
            f'{doc.get("lastname")}, {doc.get("firstname")} {doc.get("credentialnumber", [])[:2]} '
            for doc in json_results
        ]
        return Results(QueryStatus.MULTIPLE_RESULTS, notes=notes)

    dinfo = json_results[0]
    lic_status = dinfo['status'].casefold()
    
    if 'active' in lic_status:
        status = LicenseStatus.ACTIVE
    elif 'expired' in lic_status:
        status = LicenseStatus.EXPIRED
    elif 'suspended' in lic_status:
        status = LicenseStatus.SUSPENDED
    elif 'revoke' in lic_status or 'surrender' in lic_status:
        status = LicenseStatus.SURRENDERED_OR_REVOKED

    license = MedicalLicense(
        state=State.WA, 
        status=status,
        id=dinfo['credentialnumber'],
        discipline=dinfo['actiontaken'].casefold() == 'yes' 
    )
    
    results = Results(status=QueryStatus.SUCCESS, license=license)
    return results
