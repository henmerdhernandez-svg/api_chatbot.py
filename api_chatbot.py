from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/cotizacion', methods=['GET'])
def obtener_cotizacion():
    empresa = request.args.get('empresa')
    if not empresa:
        return jsonify({'error': 'Falta el parámetro empresa'}), 400
    try:
        ticker = yf.Ticker(empresa)
        data = ticker.history(period='1d')
        if data.empty:
            return jsonify({'error': 'No se encontraron datos para la empresa'}), 404
        precio_actual = data['Close'].iloc[-1]
        return jsonify({'empresa': empresa, 'precio_actual': precio_actual})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/estado_financiero', methods=['GET'])
def obtener_estado_financiero():
    empresa = request.args.get('empresa')
    if not empresa:
        return jsonify({'error': 'Falta el parámetro empresa'}), 400
    try:
        ticker = yf.Ticker(empresa)
        financials = ticker.financials
        if financials.empty:
            return jsonify({'error': 'No se encontraron estados financieros'}), 404
        financials_transpose = financials.transpose()
        return financials_transpose.to_json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/pregunta', methods=['GET'])
def responder_pregunta():
    pregunta = request.args.get('pregunta')
    if not pregunta:
        return jsonify({'error': 'Falta el parámetro pregunta'}), 400
    respuesta = f'Recibí tu pregunta sobre finanzas: {pregunta}'
    return jsonify({'respuesta': respuesta})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
