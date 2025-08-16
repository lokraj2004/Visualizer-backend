from flask import request, jsonify
from FirebaseSetup import db_firestore, db_realtime  # Make sure both are imported

def login_page():
    data = request.json
    username = data.get("username")
    user_id = data.get("id")           # clientID
    role = data.get("role")
    admin_id = data.get("adminId")     # Only for admin

    print(f"[LOGIN ATTEMPT] Role: {role}, Username: {username}, ClientID: {user_id}, AdminID: {admin_id}")

    try:
        # Step 1: Get slot info from Firestore
        slot_names = [f"slot{i}" for i in range(1, 11)]
        active_slots_ref = db_firestore.collection("slots").document("activeSlots")
        active_slots_doc = active_slots_ref.get()

        if not active_slots_doc.exists:
            print("[ERROR] activeSlots document not found.")
            return jsonify({"error": "activeSlots document not found"}), 500

        active_slots_data = active_slots_doc.to_dict()
        found = False

        # Step 2: Check if clientID and username exist in any slot
        for slot_name in slot_names:
            if slot_name in active_slots_data:
                client_data = active_slots_data[slot_name]
                print(f"[DEBUG] Checking {slot_name}: {client_data}")

                if (
                    client_data.get("clientID") == user_id and
                    client_data.get("username") == username
                ):
                    print(f"[SUCCESS] Client match found in {slot_name}")
                    found = True
                    break
            else:
                print(f"[DEBUG] {slot_name} is empty or not present.")

        if not found:
            print("[FAILED] No matching client found in any slot.")
            return jsonify({"message": "unauthorised"}), 401

        # Step 3: Handle roles
        if role == "client":
            return jsonify({"success": True, "message": "authorised"}), 200

        elif role == "admin":
            # Validate adminID from Realtime Database at /auth_key/key
            print("reactAdmin")
            print(admin_id)
            stored_admin_id = db_realtime.reference("/auth_key/key").get()
            print("StoredAdmin")
            print(stored_admin_id)

            if stored_admin_id == admin_id:
                print(f"[SUCCESS] AdminID verified.")
                return jsonify({"success": True, "message": "admin authorised"}), 200
            else:
                print(f"[FAILED] AdminID mismatch.")
                return jsonify({"success": False, "message": "invalid adminID"}), 403

        else:
            return jsonify({"error": "Unknown role"}), 400

    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"error": str(e)}), 500
