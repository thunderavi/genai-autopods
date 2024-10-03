from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL

# Initialize Blueprint
pod_routes = Blueprint('pod_routes', __name__)

# MySQL instance should be imported or initialized here
# Assuming mysql is passed or available globally

@pod_routes.route('/create-pod', methods=['POST'])
def create_pod():
    data = request.get_json()
    name = data.get('name')
    project_description = data.get('project_description')

    try:
        cur = mysql.connection.cursor()
        
        # Check if a pod with the same name already exists
        cur.execute("SELECT * FROM pods WHERE name = %s", (name,))
        existing_pod = cur.fetchone()
        
        if existing_pod:
            return jsonify({"error": "A pod with this name already exists."}), 400
        
        # Insert new pod
        cur.execute("INSERT INTO pods (name, project_description) VALUES (%s, %s)", (name, project_description))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Pod created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pod_routes.route('/pods', methods=['GET'])
def get_pods():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pods")
        pods = cur.fetchall()
        cur.close()

        # Convert pods to a list of dictionaries
        pod_list = [{"id": pod[0], "name": pod[1], "project_description": pod[2]} for pod in pods]

        return jsonify(pod_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pod_routes.route('/update-pod/<int:id>', methods=['PUT'])
def update_pod(id):
    data = request.get_json()
    name = data.get('name')
    project_description = data.get('project_description')

    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE pods SET name = %s, project_description = %s WHERE id = %s", (name, project_description, id))
        mysql.connection.commit()
        cur.close()

        if cur.rowcount == 0:
            return jsonify({"error": "Pod not found."}), 404
        
        return jsonify({"message": "Pod updated successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@pod_routes.route('/search-pod', methods=['GET'])
def search_pod():
    query = request.args.get('q')
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pods WHERE name LIKE %s", ('%' + query + '%',))
        pods = cur.fetchall()
        cur.close()

        pod_list = [{"id": pod[0], "name": pod[1], "project_description": pod[2]} for pod in pods]
        return jsonify(pod_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
