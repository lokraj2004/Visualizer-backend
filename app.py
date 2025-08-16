from flask import Flask, jsonify, request
from flask_cors import CORS
from bson.json_util import dumps
from RealtimeLineGraph import handle_line_graph_subscription
from SemiDial import semi_dial
from FullDial import get_full_dial_data
from SocketInstance import socketio  # ✅ Replaces the old circular import
from MonthlyUsage import get_usage_stats
from Login import login_page
from MultiValueCard import get_sensor_stats_by_id
from DonutChart import get_sensor_usage_counts

from UsageLineGraph import get_linegraph_data
from CustomFill import get_custom_fill_data
from SimpleCard import emit_latest_data_on_connect
from Toggle import handle_toggle
from NumericWidget import handle_numeric
from Picklist import handle_picklist_selection
from Slider import slider_value
from SpecialText import submit_text

app = Flask(__name__)
socketio.init_app(app, cors_allowed_origins="*")  # ✅ Replaces inline SocketIO
CORS(app)

# emit_latest_data_on_connect()
@app.route("/")
def home():
    return "Flask-MongoDB backend is running."

@app.route("/api/picklist", methods=["POST"])
def picklist():
    data = request.json
    return jsonify(handle_picklist_selection(data))

@app.route('/api/semi-dial', methods=['POST'])
def semiDial():
    return semi_dial()

@app.route("/api/submit-text", methods=["POST"])
def specialtext():
    return submit_text()

@app.route("/api/slider-value", methods=["POST"])
def slider():
    return slider_value()

@app.route("/api/toggle", methods=["GET", "POST"])
def toggle_route():
    return jsonify(handle_toggle(request))

@app.route("/api/numeric", methods=["POST"])
def numeric_route():
    return jsonify(handle_numeric(request))

@app.route("/api/custom-fill", methods=["POST"])
def custom_fill():
    return get_custom_fill_data()
@app.route("/api/full-dial", methods=["POST"])
def full_dial():
    return get_full_dial_data()

@app.route('/api/usage_stats/<view_type>', methods=['GET'])
def usage_stats(view_type):
    sensor_query = request.args.get('sensors')
    if not sensor_query:
        return jsonify({"error": "Missing sensor ID(s)"}), 400

    try:
        stats = get_usage_stats(sensor_query, view_type)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/login", methods=["POST"])
def login():
    return login_page()

@app.route("/api/donut-usage", methods=["POST"])
def donut_chart_data():
    data = request.json
    sensor_ids = data.get("sensorIds", "")

    usage_data, error = get_sensor_usage_counts(sensor_ids)
    if error:
        return jsonify({"success": False, "error": error}), 400

    return jsonify({"success": True, "data": usage_data})

@app.route('/api/sensor_stats/<int:sensor_id>')
def sensor_stats(sensor_id):
    stats = get_sensor_stats_by_id(sensor_id)
    if not stats:
        return jsonify({"error": "Invalid sensor ID"}), 400
    return jsonify(stats)

@app.route("/api/linegraph", methods=["GET"])
def linegraph_data():
    return get_linegraph_data()

if __name__ == "__main__":
    socketio.run(app, debug=True)  # ✅ Keep using socketio.run

