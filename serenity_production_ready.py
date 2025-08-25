#!/usr/bin/env python3
"""
PRODUCTION-READY SERENITY EMAIL CAPTURE SYSTEM
Optimized for reliability with timeout handling and fallback
"""

import requests
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

class ProductionSerenityEmailSystem:
    """Production-ready email system with timeout handling"""
    
    def __init__(self):
        self.api_key = "api-F7FC4178E29740E0878A2922145140F4"
        self.api_url = "https://api.smtp2go.com/v3/email/send"
        self.target_emails = ["donvon@vonbase.com", "support@vonbase.com"]
        self.sender_email = "donvon@vonbase.com"
        
    def send_email_async(self, phone: str, customer_data: dict) -> None:
        """Send email in background thread to avoid blocking"""
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            device_info = customer_data.get('device_type', 'unknown')
            
            email_body = f"""NEW CUSTOMER - Serenity Atlanta QR Menu

📱 Phone: {phone}
⏰ Time: {timestamp}
📱 Device: {device_info}
🌐 Source: QR Menu System

This customer is ready to order from Serenity Atlanta!

---
Serenity QR Menu System
Powered by VBE"""

            email_data = {
                "api_key": self.api_key,
                "to": self.target_emails,
                "sender": self.sender_email,
                "subject": f"🍽️ New Serenity Customer: {phone}",
                "text_body": email_body
            }
            
            # Send with timeout
            response = requests.post(
                self.api_url,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(email_data),
                timeout=10  # 10 second timeout
            )
            
            print(f"📧 Email sent for {phone}: {response.status_code}")
            
        except Exception as e:
            print(f"❌ Email error for {phone}: {e}")
            # Log error but don't crash the system
    
    def capture_customer(self, phone: str, customer_data: dict) -> dict:
        """Capture customer and send email asynchronously"""
        
        # Start email sending in background
        email_thread = threading.Thread(
            target=self.send_email_async,
            args=(phone, customer_data)
        )
        email_thread.daemon = True
        email_thread.start()
        
        # Return immediately to customer
        return {
            "success": True,
            "message": "Customer captured successfully",
            "phone": phone,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "email_status": "sending_in_background",
            "targets": self.target_emails
        }

# Global email system
email_system = ProductionSerenityEmailSystem()

@app.route('/capture-phone', methods=['POST'])
def capture_phone():
    """Fast customer capture endpoint"""
    
    try:
        data = request.get_json()
        phone = data.get('phone')
        customer_data = data.get('customer_data', {})
        
        if not phone:
            return jsonify({"error": "Phone number required"}), 400
        
        print(f"📞 Capturing customer: {phone}")
        
        # Capture customer (fast response)
        result = email_system.capture_customer(phone, customer_data)
        return jsonify(result), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "serenity-production"}), 200

@app.route('/', methods=['GET'])
def status():
    """System status"""
    return jsonify({
        "service": "Serenity Production Email System",
        "status": "operational",
        "targets": ["donvon@vonbase.com", "support@vonbase.com"],
        "features": ["async_email", "timeout_handling", "fast_response"]
    }), 200

if __name__ == '__main__':
    print("🍽️ SERENITY PRODUCTION EMAIL SYSTEM")
    print("=" * 40)
    print("📧 Targets: donvon@vonbase.com, support@vonbase.com")
    print("⚡ Mode: Production (fast response + background email)")
    print("🎯 Status: READY")
    print("\n🚀 Starting production server...")
    
    app.run(host='0.0.0.0', port=5000, debug=False)  # Production mode