import logging
import time

from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from re import match
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet


_log = logging.getLogger(__name__)


APP_COLUMNS = ["C","D","E","F"]
APP_ROWS = [25, 26, 27, 28, 29]
FORM_CURRENT = "Geoclient API"
FORM_LEGACY = "Geoclient API - v1"
MISSING_EMAIL = "N/A"
ROLE_SPONSOR = "Sponsor"
ROLE_SUPPORT = "Support"
ROLE_TEAM_DEFAULT = "Team"


@dataclass
class Contact:
    """Generic record-like object for contact information."""
    email: str
    name: str = None
    phone: str = None
    role: str = None

    def has_info(self) -> bool:
        return self.email is not None or self.name is not None or self.phone is not None

@dataclass
class Application:
    """Container for an application's contact information."""
    name: str
    group: Contact = None
    team: list[Contact] = field(default_factory=list)
    sponsor: Contact = None

def contains_email(text):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if match(pattern, text):
        return True
    else:
        return False

def get_xlsx_paths():
    directory = Path("./source/xlsx/")
    xlsx_files = sorted(directory.rglob("*.xlsx"))
    return xlsx_files

def _cval(ws: Worksheet, cell: str, default_value=None):
    if ws is None:
        return default_value
    c = ws[cell]
    if c is None:
        return default_value
    v = c.value
    if v is None:
        return default_value
    return v

def _get_group(ws: Worksheet):
    """
    Gets the distribution list contact info.
    Only applies to the current form.

    C23 - group email
    D23 - group name
    E23 - group phone

    Parameters
    ----------
    ws: Worksheet

    Returns
    -------
    Contact
    """
    contact = Contact(_cval(ws, "C23", MISSING_EMAIL), _cval(ws, "D23"), _cval(ws, "E23"), ROLE_SUPPORT)
    if not contact.has_info():
        return None
    return contact

def _get_sponsor(ws: Worksheet):
    """
    Gets the project sponsor contact info.
    Only applies to the current form.

    C18 - name
    D18 - email
    E18 - phone
    F18 - title

    Parameters
    ----------
    ws: Worksheet

    Returns
    -------
    Contact
    """
    contact = Contact(_cval(ws, "D18", MISSING_EMAIL), _cval(ws, "C18"), _cval(ws, "E18"), _cval(ws, "F18", ROLE_SPONSOR))
    if not contact.has_info():
        return None
    return contact

def _get_team(ws: Worksheet):
    """
    Gets the project application team members contact info.
    Only applies to the current form.

    C25:F29
    Cxx - name
    Dxx - email
    Exx - phone
    Fxx - role

    Parameters
    ----------
    ws: Worksheet

    Returns
    -------
    list of Contact
    """
    team_members = []
    for row in APP_ROWS:
        email = None
        name = None
        phone = None
        role = None
        for col in APP_COLUMNS:
            match col:
                case "C":
                    name = _cval(ws,f"{col}{row}")
                case "D":
                    email = _cval(ws,f"{col}{row}", MISSING_EMAIL)
                case "E":
                    phone = _cval(ws,f"{col}{row}")
                case "F":
                    role = _cval(ws,f"{col}{row}", ROLE_TEAM_DEFAULT)
                case _:
                    raise ValueError(f"Unexpected column {col}.")
        contact = Contact(email, name, phone, role)
        if contact.has_info():
            team_members.append(contact)
    return team_members

def export(excel_file: Path):
    """
    Extracts contact information from Excel file.

    Distinguishes between a "current" signup form and a "legacy" (v1) form
    in order to extract data from the proper cell locations.
    
    If B3 contains "Geoclient API - v1",
    then it is a legacy form. If B3 is "Geoclient API", then it is the
    current form.
    """
    wb = load_workbook(excel_file, True, False, True)
    ws = wb["Request Form"]
    #print("------------------------------------------------------------------------------")
    if ws["B3"].value == FORM_CURRENT:
        sponsor = _get_sponsor(ws)
        team = _get_team(ws)
        group = _get_group(ws)
        app = Application(excel_file.stem, group, team, sponsor)
        print(app)
    elif ws["B3"].value == FORM_LEGACY:
        print(f"{excel_file.stem} - legacy form")
    else:
        print(f"{excel_file.stem} - ERROR")

def main():
    logging.basicConfig(level=logging.WARNING)

    xlsx_paths = get_xlsx_paths()
    for excel_file in xlsx_paths:
        export(excel_file)


if __name__ == "__main__":
    main()
