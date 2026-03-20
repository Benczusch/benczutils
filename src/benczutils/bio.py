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

# Stop Codon: X
CODON_TABLE = {
    "UUU": "F",      "CUU": "L",      "AUU": "I",      "GUU": "V",
    "UUC": "F",      "CUC": "L",      "AUC": "I",      "GUC": "V",
    "UUA": "L",      "CUA": "L",      "AUA": "I",      "GUA": "V",
    "UUG": "L",      "CUG": "L",      "AUG": "M",      "GUG": "V",
    "UCU": "S",      "CCU": "P",      "ACU": "T",      "GCU": "A",
    "UCC": "S",      "CCC": "P",      "ACC": "T",      "GCC": "A",
    "UCA": "S",      "CCA": "P",      "ACA": "T",      "GCA": "A",
    "UCG": "S",      "CCG": "P",      "ACG": "T",      "GCG": "A",
    "UAU": "Y",      "CAU": "H",      "AAU": "N",      "GAU": "D",
    "UAC": "Y",      "CAC": "H",      "AAC": "N",      "GAC": "D",
    "UAA": "X",      "CAA": "Q",      "AAA": "K",      "GAA": "E",
    "UAG": "X",      "CAG": "Q",      "AAG": "K",      "GAG": "E",
    "UGU": "C",      "CGU": "R",      "AGU": "S",      "GGU": "G",
    "UGC": "C",      "CGC": "R",      "AGC": "S",      "GGC": "G",
    "UGA": "X",      "CGA": "R",      "AGA": "R",      "GGA": "G",
    "UGG": "W",      "CGG": "R",      "AGG": "R",      "GGG": "G", 
}

class MotifNotation:
    def __init__(self, notation_type, content):
        # notation type: 1 - positive ('A' or '[AB]')
        #                2 - negative ('{C}')
        self.notation_type = notation_type
        self.content = content
    def check(self, char):
        if self.notation_type == 1:
            return char in self.content
        else:
            return char not in self.content

class Motif:
    def __init__(self, motif_string):
        self.motif_list = []
        string_working = list(motif_string)
        while len(string_working) > 0:
            nextChar = string_working.pop(0)
            if nextChar == '{':
                segmentEnd = string_working.index('}')
                segment = string_working[:segmentEnd]
                string_working = string_working[segmentEnd + 1:]
                self.motif_list.append(MotifNotation(2, segment))
            elif nextChar == '[':
                segmentEnd = string_working.index(']')
                segment = string_working[:segmentEnd]
                string_working = string_working[segmentEnd + 1:]
                self.motif_list.append(MotifNotation(1, segment))
            else:
                self.motif_list.append(MotifNotation(1, [nextChar]))
        self.motif_length = len(self.motif_list)
    def check(self, comparison):
        if len(comparison) != self.motif_length:
            return False
        for i in range(self.motif_length):
            if not self.motif_list[i].check(comparison[i]):
                return False
        return True
