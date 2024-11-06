from flask import Flask, render_template, request
from maquina_ajedrez import MaquinaTuring

app = Flask(__name__)
maquina = MaquinaTuring('MT.xml')

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = ""

    if request.method == 'POST':
        cadena = request.form["cadena"]
        # resultados = maquina.validarCadena(cadena)
        resultados = validar_cadena_temporal(cadena) 

    return render_template("index.html", resultados=resultados)

def validar_cadena_temporal(cadena):
    return f"Cadena '{cadena}' recibida exitosamente"

if __name__ == "__main__":
    app.run(debug=True)
