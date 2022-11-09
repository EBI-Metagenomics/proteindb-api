from pydantic import BaseModel


class Study(BaseModel):
    id: int
    accession: str

    class Config:
        orm_mode = True


class Assembly(BaseModel):
    id: int
    accession: str
    pipeline_version: str

    class Config:
        orm_mode = True


class Biome(BaseModel):
    lineage: str

    class Config:
        orm_mode = True


class Contig(BaseModel):
    id: int
    kmer_coverage: int
    length: int
    contig_name: str | None = None

    class Config:
        orm_mode = True


class Protein(BaseModel):
    id: int
    digest: str
    sequence: str
    private: bool

    class Config:
        orm_mode = True


class ProteinMetadata(BaseModel):
    id: int
    protein: Protein
    caller: str
    start_protein: int
    end_protein: int
    strand: str

    contig: Contig
    assembly: Assembly

    class Config:
        orm_mode = True


Protein.update_forward_refs()
