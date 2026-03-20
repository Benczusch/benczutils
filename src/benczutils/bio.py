import requests

def getFasta(protId):
    result = requests.get(f"http://www.uniprot.org/uniprot/{protId}.fasta")

    return readFasta(result.text)

def readFasta(text):
    genes = {}
    current = ""
    for line in text.splitlines():
        if len(line) < 1:
            continue
        elif line[0] == '>':
            current = line[1:]
            genes[current] = ""
        else:
            genes[current] += line
    
    return genes