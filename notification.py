from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="income_panel"
    )

# Endpoint to get all notifications
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC")
    notifications = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(notifications), 200

# Endpoint to get unread notifications
@app.route('/api/notifications/unread', methods=['GET'])
def get_unread_notifications():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM notifications WHERE status = 'unread' ORDER BY created_at DESC")
    notifications = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(notifications), 200

# Endpoint to mark a notification as read
@app.route('/api/notifications/mark-as-read/<int:notification_id>', methods=['PUT'])
def mark_as_read(notification_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE notifications SET status = 'read' WHERE notification_id = %s", (notification_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Notification marked as read"}), 200

# Endpoint to delete a specific notification
@app.route('/api/notifications/delete/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM notifications WHERE notification_id = %s", (notification_id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Notification deleted"}), 200

# Endpoint to clear all notifications
@app.route('/api/notifications/clear-all', methods=['DELETE'])
def clear_all_notifications():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM notifications")
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "All notifications cleared"}), 200

if __name__ == '__main__':
    app.run(debug=True)
