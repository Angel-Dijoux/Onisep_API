from dataclasses import dataclass
import strawberry


@dataclass
@strawberry.type
class Job:
    id: str
    libelle: str


def process_jobs(jobs: list[dict]) -> list[Job]:
    if jobs:
        jobs = jobs if isinstance(jobs, list) else [jobs]
        return [
            Job(
                id=item["id"],
                libelle="·".join(part.strip() for part in item["libelle"].split("/")),
            )
            for item in jobs
        ]
