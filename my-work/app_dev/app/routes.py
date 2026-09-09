from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.agents.orchestrator_agent import OrchestratorAgent
from app.services.booking_service import BookingService

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/request', methods=['POST'])
def submit_request():
    session['request_data'] = {
        'problem': request.form.get('problem'),
        'location': request.form.get('location'),
        'preferred_date': request.form.get('preferred_date'),
        'preferred_time': request.form.get('preferred_time')
    }
    return redirect(url_for('main.processing'))

@bp.route('/processing')
def processing():
    if 'request_data' not in session:
        return redirect(url_for('main.index'))
    return render_template('processing.html')

@bp.route('/api/process', methods=['POST'])
def process_pipeline():
    data = session.get('request_data')
    if not data:
        return jsonify({"success": False, "error": "No request data."}), 400

    # Delegate entirely to the Root Orchestrator Agent
    orchestrator = OrchestratorAgent()
    result = orchestrator.run(
        problem=data.get('problem'),
        location=data.get('location'),
        preferred_date=data.get('preferred_date'),
        preferred_time=data.get('preferred_time'),
    )

    if not result.get("success"):
        return jsonify(result), 400

    session['service_request'] = result.get("service_request")
    session['recommendations'] = result.get("providers", [])

    return jsonify({"success": True})

@bp.route('/recommendations')
def recommendations():
    providers = session.get('recommendations', [])
    if not providers:
        # if not processed yet, or empty
        pass
    return render_template('recommendations.html', providers=providers, service_request=session.get('service_request'))

@bp.route('/book', methods=['POST'])
def book():
    provider_id = request.form.get('provider_id')
    service_request = session.get('service_request')
    
    if not provider_id or not service_request:
        return render_template('error.html', message="Missing booking information.")
        
    booking_service = BookingService()
    result = booking_service.create_booking(provider_id, service_request)
    
    if result.get("success"):
        session['booking_result'] = result
        return redirect(url_for('main.confirmation', booking_id=result.get("booking_id")))
    else:
        return render_template('error.html', message=result.get("error", "Booking failed."))

@bp.route('/confirmation/<booking_id>')
def confirmation(booking_id):
    result = session.get('booking_result')
    if not result or result.get("booking_id") != booking_id:
        return redirect(url_for('main.index'))
    return render_template('confirmation.html', booking=result)
