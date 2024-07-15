from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Diccionario de provincias
provincias = {
    "EC-A": "AZUAY",
    "EC-B": "BOLIVAR",
    "EC-F": "CAÑAR",
    "EC-C": "CARCHI",
    "EC-H": "CHIMBORAZO",
    "EC-X": "COTOPAXI",
    "EC-O": "EL ORO",
    "EC-E": "ESMERALDAS",
    "EC-W": "GALAPAGOS",
    "EC-G": "GUAYAS",
    "EC-I": "IMBABURA",
    "EC-L": "LOJA",
    "EC-R": "LOS RIOS",
    "EC-M": "MANABI",
    "EC-S": "MORONA SANTIAGO",
    "EC-N": "NAPO",
    "EC-D": "ORELLANA",
    "EC-Y": "PASTAZA",
    "EC-P": "PICHINCHA",
    "EC-SE": "SANTA ELENA",
    "EC-SD": "SANTO DOMINGO DE LOS TSACHILAS",
    "EC-U": "SUCUMBIOS",
    "EC-T": "TUNGURAHUA",
    "EC-Z": "ZAMORA CHINCHIPE"
}

@app.route('/verifica', methods=['GET'])
def verifica():
    codigo_postal = request.args.get('codigo_postal')
    code = request.args.get('code')
    
    if not codigo_postal or not code:
        return jsonify({"error": "Faltan parámetros"}), 400

    if code not in provincias:
        return jsonify({"error": "Código de provincia no válido"}), 400

    provincia_esperada = provincias[code]

    url = f"https://www.codigopostal.gob.ec/js/ec/gob/anp/visor/server/GeometriasJson.php?codigoPostal={codigo_postal}&metodo=getZonaPostal"

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        data = response.json()

        if "data" not in data:
            return jsonify({"data": False})

        if data["data"] == False:
            return jsonify({"data": False})

        for item in data["data"]:
            if item["provincia"].upper() == provincia_esperada:
                return jsonify({"data": True})

        return jsonify({"data": False})
    
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
