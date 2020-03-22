from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
URL_BASE = 'localhost:5000'
# SWAGGER
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Images classification V1"
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# END SWAGGER

@app.route('/')
def hello_world():
    return 'Images classification V1'


@app.route('/uploads', methods=['POST'])
def upload_files():
    return 'Files uploaded', 201


@app.route('/classified_folders',  methods=['GET'])
def classified_folders():
    data = {
        'invoices': {
            'total': 321,
            'add': 11
        },
        'air_manifest': {
            'total': 500,
            'add': 25
        },
        'Handwritten': {
            'total': 121,
            'add': 32
        },
        'unlabeled': {
            'total': 352,
            'add': 20
        },
        'budget': {
            'total': 43,
            'add': 8
        },
        'form': {
            'total': 200,
            'add': 4
        }
    }
    return jsonify(data), 200


@app.route('/all_documents', methods=['GET'])
def all_documents():
    pass


@app.route('/invoices', methods=['GET'])
def list_invoices():
    data = { 'name': 'file.png', 'date':"", 'siren': True, 'tva': True, 'adresse': False, 'url': URL_BASE+'/static/invoices/invoice.jfif'}
    return jsonify([data])


@app.route('/air_manifests', methods=['GET'])
def list_air_manifest():
    return jsonify([])


@app.route('/unlabeled', methods=['GET'])
def list_unlabeled():
    return jsonify([])


@app.route('/budgets', methods=['GET'])
def list_budget():
    return jsonify([])


@app.route('/forms', methods=['GET'])
def list_form():
    return jsonify([])


@app.route('/Handwritten', methods=['GET'])
def list_Handwrite():
    return jsonify([])


if __name__ == '__main__':
    app.run(debug=True)
