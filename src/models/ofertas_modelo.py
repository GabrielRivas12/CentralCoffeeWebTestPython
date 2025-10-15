from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Oferta:
    """
    Representa una oferta de café. El uso de dataclass simplifica la creación
    de la clase y proporciona métodos como __init__ y __repr__ automáticamente.
    """

    # clase sin usar por el momento
    titulo: str
    tipoCafe: str
    variedad: str
    clima: str
    fechaCosecha: str
    altura: str
    cantidadProduccion: str
    estadoGrano: str
    procesoCorte: str
    ofertaLibra: str
    lugarSeleccionado: str
    userId: str
    nuevo: bool = False
    imagen: Optional[str] = ""
    id: Optional[str] = None

    def to_dict(self):
        """Convierte el objeto Oferta a un diccionario, excluyendo el id."""
        data = asdict(self)
        del data['id'] # El id no se guarda como un campo en el documento de Firestore
        return data

    @classmethod
    def from_dict(cls, source: dict, doc_id: str):
        """Crea una instancia de Oferta desde un diccionario de Firestore."""
        # Filtra los campos extra que puedan venir de Firestore y no esten en la clase
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_source = {k: v for k, v in source.items() if k in known_fields}
        
        oferta = cls(**filtered_source)
        oferta.id = doc_id
        return oferta

