from rdkit import Chem
from rdkit.Chem import Draw
from io import StringIO
import requests
import sys
import os
from flask import Flask,request,send_file,jsonify
app = Flask(__name__)
Chem.WrapLogs()

@app.route("/",methods=["GET"])
def draw():
    if request.method == 'GET':
        mol_smile = request.args.get('smile')
        try:
            sio = sys.stderr = StringIO()
            mol = Chem.MolFromSmiles(mol_smile)
            Draw.MolToImageFile(mol,filename="img.png",size = (200,200))
        except:
            if "SMILES Parse Error" in sio.getvalue():
                return jsonify(
                    error="SMILES Parsing Error"
                )
            else:
                return jsonify(
                    error = "Unidentified Error"
                )
    return send_file("img.png",mimetype='image/png')
@app.route("/describe",methods=["GET"])
def describe():
    if request.method == 'GET':
        mol_smile = request.args.get('smile')
        try:
            sio = sys.stderr = StringIO()
            mol = Chem.MolFromSmiles(mol_smile)
            numAtoms = mol.GetNumAtoms()
            numBonds = mol.GetNumBonds()
            res = requests.get(f"https://cactus.nci.nih.gov/chemical/structure/{mol_smile}/iupac_name")
        except:
            if "SMILES Parse Error" in sio.getvalue():
                return jsonify(
                    error="SMILES Parsing Error"
                )
            else:
                return jsonify(
                    error = "Unidentified Error"
                )
    return jsonify(
            molname = res.text,
            atoms = numAtoms,
            bonds = numBonds,
        )
if __name__ == "__main__":
    app.run(port=int(os.getenv('PORT')),debug=True) 