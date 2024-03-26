import time
from datetime import datetime, timedelta

import pandas
from requests import Session, Request

from exceptions import *
from settings import DOWNLOADS, DATABASE_FRESHNESS_DAYS
from medicalboards import StateMedicalBoardInterface
from medicalboards.states import State
from enums_and_dataclasses import (
    Doctor, 
    LicenseStatus, 
    Result,
    ResultStatus,
    MedicalLicense
)

class MedicalBoardInterface(StateMedicalBoardInterface):
    state = State.AK
    downloads = DOWNLOADS / "ak"
    db_file_path = downloads / "db.csv"
    database_url = ("https://www.commerce.alaska.gov/cbp/DBDownloads/"
                    "ProfessionalLicenseDownload.CSV")

    @classmethod
    def _download_database(cls) -> None:
        cls.downloads.mkdir(parents=True, exist_ok=True)
        if cls.db_file_path.exists():
            cls.db_file_path.unlink()

        with Session() as session, open(cls.db_file_path, "xb") as file:
            request = Request("GET", cls.database_url).prepare()
            resp = session.send(request, timeout=60)
            resp.raise_for_status()
            file.write(resp.content)

    @classmethod
    def _database_age(cls) -> timedelta:
        now_unixtime = int(time.time())
        file_edit_time = 0 if not cls.db_file_path.exists() \
                        else int(cls.db_file_path.stat().st_mtime)
        delta_seconds = now_unixtime - file_edit_time
        return timedelta(seconds=delta_seconds)

    @classmethod
    def _db_is_fresh(cls) -> bool:
        return (cls._database_age().days < DATABASE_FRESHNESS_DAYS
                and cls.db_file_path.stat().st_size > 1_000_000)

    @classmethod
    def license_search(cls, doctor: Doctor) -> Result: 
        result = Result()
        if not cls._db_is_fresh():
            cls._download_database()

        df = pandas.read_csv(cls.db_file_path, usecols=[
            "Program", "ProfType", "LicenseNum", "Owners", "Status"
        ])

        df = df[
            (df["Program"] == "Medical") 
            & (df["ProfType"].str.lower().str.contains("physician|podiatrist"))
            & (df["Owners"].str.lower().str.contains(doctor.lastname))
        ]
        if doctor.firstname:
            df = df[df["Owners"].str.lower().str.contains(doctor.firstname)]
        if doctor.middle:
            df = df[df["Owners"].str.lower().str.contains(doctor.lastname)]
        print(df)
        if len(df) != 1:
            if not len(df):
                result.status = ResultStatus.NOT_FOUND
            else:
                result.status = ResultStatus.MULTIPLE_RESULTS
                for row in df:
                    result.notes.append(str(row))
            return result
        row_values = df.iloc[0]
        licstatus = row_values['Status'].casefold()

        result.license = MedicalLicense(
            State.AK,
            status=(LicenseStatus.ACTIVE if 'active' in licstatus
                    else LicenseStatus.EXPIRED if 'inactive' in licstatus
                    else LicenseStatus.EXPIRED if 'retired' in licstatus
                    else LicenseStatus.SUSPENDED if 'suspended' in licstatus
                    else LicenseStatus.OTHER),
            id=row_values['LicenseNum'],
            discipline=False
        )
        result.status = ResultStatus.INCOMPLETE
        result.notes.append(
            "WARNING - UNABLE TO VERIFY IF DOCTOR HAS BEEN DISCIPLINED\n"
            "The Alaska Dept. of Commerce, Community, and Economic "
            "Development does not include disciplinary action in their public "
            "downloadable database, and to check for that you have to pass a "
            "CAPTCHA. To see if your doctor is bad, you will need to check "
            "yourself at: "
            "https://www.commerce.alaska.gov/cbp/main/Search/Professional\n"
            "To contact the board and give them your thoughts on how to do "
            "better (like provide this data in the downloadable database) "
            "go here: "
            "https://www.commerce.alaska.gov/cbp/main/Search/ContactForm"
        )
        return result