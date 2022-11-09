from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db

# TODO: install and configure
# from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()


@app.get("/proteins/", response_model=list[schemas.Protein])
def get_proteins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    proteins = (
        db.query(models.Protein)
        .filter(models.Protein.private != False)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return proteins


@app.get("/proteins/{mgyp}", response_model=schemas.Protein)
def get_protein(mgyp: str, db: Session = Depends(get_db)):
    """Fetch a protein by accession"""
    mgyp_id = int(mgyp.replace("MGYP", ""))
    return db.query(models.Protein).filter(models.Protein.id == mgyp_id).first()


@app.get("/proteins/{mgyp}/metadata", response_model=list[schemas.ProteinMetadata])
def get_protein_metadata(
    mgyp: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """Fetch the metadata for a protein accession"""
    mgyp_id = int(mgyp.replace("MGYP", ""))

    protein_metadata = (
        db.query(models.ProteinMetadata)
        .filter(models.ProteinMetadata.mgyp_id == mgyp_id)
        # .filter(models.ProteinMetadata.public == "public") # TODO: check this one with Kate / Juan
        .offset(skip)
        .limit(limit)
        .all()
    )
    return protein_metadata


@app.get("/proteins/{mgyp}/biomes", response_model=list[schemas.Biome])
def get_protein_biomes(
    mgyp: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """Fetch the biomes related to a protein accession"""
    mgyp_id = int(mgyp.replace("MGYP", ""))

    biomes = (
        db.query(models.Biome)
        .join(models.Assembly, models.Assembly.biome_id == models.Biome.id)
        .join(
            models.ProteinMetadata,
            models.Assembly.id == models.ProteinMetadata.assembly_id,
        )
        .distinct()
        .offset(skip)
        .limit(limit)
        .all()
    )
    return biomes


@app.get("/proteins/{mgyp}/studies", response_model=list[schemas.Study])
def get_protein_studies(
    mgyp: str,
    study: str = "",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Fetch the studies related to a protein accession"""
    mgyp_id = int(mgyp.replace("MGYP", ""))

    studies = (
        db.query(models.Study)
        .join(models.Assembly, models.Assembly.study_id == models.Study.id)
        .join(
            models.ProteinMetadata,
            models.ProteinMetadata.assembly_id == models.Assembly.id,
        )
        .filter(models.ProteinMetadata.mgyp_id == mgyp_id)
        .distinct()
        .offset(skip)
        .limit(limit)
        .all()
    )
    return studies


@app.get(
    "/proteins/{mgyp}/studies/{study_accession}/assemblies",
    response_model=list[schemas.Assembly],
)
def get_protein_assemblies(
    mgyp: str,
    study_accession: str = "",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Fetch the assemblies for a given study and protein"""
    mgyp_id = int(mgyp.replace("MGYP", ""))

    assemblies = (
        db.query(models.Assembly)
        .join(models.Study, models.Study.id == models.Assembly.study_id)
        .join(
            models.ProteinMetadata,
            models.ProteinMetadata.assembly_id == models.Assembly.id,
        )
        .filter(models.ProteinMetadata.public == "public")
        .filter(models.ProteinMetadata.mgyp_id == mgyp_id)
        .filter(models.Study.accession == study_accession)
        .distinct()
        .offset(skip)
        .limit(limit)
        .all()
    )
    return assemblies


@app.get("/assemblies/{assembly_accession}/contigs", response_model=list[schemas.Contig])
def get_assembly_contigs(
    assembly_accession: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    contigs = (
        db.query(models.Contig)
        .join(models.Assembly, models.Assembly.id == models.Contig.assembly_id)
        .filter(models.Assembly.accession == assembly_accession)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return contigs


@app.get("/contigs/{mgyc}", response_model=schemas.Contig)
def get_contig(mgyc: int, db: Session = Depends(get_db)):
    contig = db.query(models.Contig).filter(models.Contig.id == mgyc).first()
    return contig
