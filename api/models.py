import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship

from .database import Base


class Protein(Base):
    __tablename__ = "protein"

    id = Column(Integer, primary_key=True, index=True)
    digest = Column(String, primary_key=True, index=True)
    sequence = Column(String, unique=False, index=False)
    private = Column(Boolean, unique=False, index=False)

    protein_metadata = relationship(
        "ProteinMetadata",
        foreign_keys=[id],
        primaryjoin="ProteinMetadata.mgyp_id == Protein.id",
        uselist=False,
    )


class ProteinCallerEnum(enum.Enum):
    prodigal_263 = "Prodigal_2.6.3"
    fgs_131 = "fgs_1.31"
    fgs_120 = "fgs_1.20"


class StrandEnum(enum.Enum):
    positive = 1
    negative = -1


class PublicEnum(enum.Enum):
    public = "public"
    private = "private"


class PartialEnum(enum.Enum):
    partial = "partial"
    full = "full"


class ProteinMetadata(Base):
    __tablename__ = "protein_metadata"

    id = Column(Integer, primary_key=True, index=True)
    mgyp_id = Column(Integer)
    protein = relationship(
        "Protein",
        foreign_keys=[mgyp_id],
        primaryjoin="Protein.id == ProteinMetadata.mgyp_id",
    )
    mgyc_id = Column(Integer, ForeignKey("contig.id"))
    contig = relationship("Contig")

    assembly_id = Column(Integer, ForeignKey("assembly.id"))
    assembly = relationship("Assembly")

    # TODO: Use Enum
    partial = Column(String)  # Enum(PartialEnum))
    public = Column(String)  # Enum(PublicEnum))
    caller = Column(String)  # Enum(ProteinCallerEnum)

    start_protein = Column(Integer)
    end_protein = Column(Integer)
    # TODO: Use Enum
    strand = Column(String)  # Enum(StrandEnum)


class Study(Base):
    __tablename__ = "study"

    id = Column(Integer, primary_key=True, index=True)
    accession = Column(String)
    public = Column(Boolean)

    assemblies = relationship("Assembly", back_populates="study")


class Assembly(Base):
    __tablename__ = "assembly"

    id = Column(Integer, primary_key=True, index=True)
    accession = Column(String)
    # TODO: Fill this information from mgnify
    # mgnify_accession = Column(String, unique)
    study_id = Column(Integer, ForeignKey("study.id"))
    study = relationship("Study", back_populates="assemblies")
    
    biome_id = Column(Integer, ForeignKey("biomes.id"))
    biome = relationship("Biome")

    contigs = relationship("Contig", back_populates="assembly")

    pipeline_version = Column(Integer)


class Contig(Base):
    __tablename__ = "contig"

    id = Column(Integer, primary_key=True, index=True)
    digest = Column(String(length=255), unique=True, index=True)
    kmer_coverage = Column(Integer, nullable=True)
    length = Column(Integer, nullable=True)
    contig_name = Column(String)

    assembly_id = Column(Integer, ForeignKey("assembly.id"))
    assembly = relationship("Assembly", back_populates="contigs")


class Biome(Base):
    __tablename__ = "biomes"

    id = Column(Integer, primary_key=True, index=True)
    lineage = Column(String(length=255))
