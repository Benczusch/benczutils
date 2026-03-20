import requests

def getFasta(protId):
    result = requests.get(f"http://www.uniprot.org/uniprot/{protId}.fasta")
    if result.status_code != 200:
        raise Exception(f"Failed to fetch FASTA for {protId}: {result.status_code}")

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