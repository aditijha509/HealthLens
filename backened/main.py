from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from Bio import Entrez, SeqIO
Entrez.email = "student@test.com"
app = FastAPI()
# --- THIS IS THE CORS BLOCK THAT WAS MISSING ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"app":"healthlens","status": "running"}

@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    # This reads the CSV in one single step
    df = pd.read_csv(file.file)
    
    row_count = df.shape[0]
    col_count = df.shape[1]
    
    return {
        "file": file.filename,
        "row": row_count,
        "column": col_count,
        "column_name":list(df.columns),
        "missing":int(df.isnull().sum().sum())
    }
@app.get("/gene/{gene_name}")
def search_gene(gene_name: str):
    try:
        search_handle=Entrez.esearch(db='nucleotide', term=f"{gene_name}[Gene] AND human[Organism]", retmax=1)
        search_result=Entrez.read(search_handle) #convert messy handler to python dict
        if not search_result["IdList"]:
            raise HTTPException( 
                                status_code=400,
                                detail=f"gene {gene_name} does not exists")
        serial_number=search_result["IdList"][0]
        
        fetch_handle=Entrez.efetch(db="nucleotide", id=serial_number , rettype="gb" , retmode="text")
        record = SeqIO.read(fetch_handle, "genbank")
        dna_sequence=str(record.seq)
        return {
                "searched_name": gene_name,
                "serial_number": serial_number,
                "description": record.description,
                "length": len(dna_sequence),
                "A": dna_sequence.count("A"),
                "T": dna_sequence.count("T"),
                "C": dna_sequence.count("C"),
                "G": dna_sequence.count("G")
            }
    except HTTPException as error:
        raise error 
    except Exception as e:
        raise HTTPException(status_code=500, detail="database error")
    