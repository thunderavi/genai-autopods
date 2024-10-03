
from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from routes.pod_routes import pod_routes


app = Flask(__name__)

app.config.from_object(Config)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Helpforu@09'
app.config['MYSQL_DB'] = 'autopods_db'  # Replace with your actual database name

mysql = MySQL(app)

app.register_blueprint(pod_routes)



@app.route('/create-pod', methods=['POST'])
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
    

@app.route('/pods', methods=['GET'])
def get_pods():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pods")
        pods = cur.fetchall()
        cur.close()

        # Convert pods to a list of dictionaries
        pod_list = []
        for pod in pods:
            pod_dict = {
                "id": pod[0],
                "name": pod[1],
                "project_description": pod[2]
            }
            pod_list.append(pod_dict)

        return jsonify(pod_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/search-pod', methods=['GET'])
def search_pod():
    query = request.args.get('q')
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pods WHERE name LIKE %s", (f'%{query}%',))
        pods = cur.fetchall()
        cur.close()

        pod_list = []
        for pod in pods:
            pod_dict = {
                "id": pod[0],
                "name": pod[1],
                "project_description": pod[2]
            }
            pod_list.append(pod_dict)

        return jsonify(pod_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update-pod/<int:pod_id>', methods=['PUT'])
def update_pod(pod_id):
    data = request.get_json()
    name = data.get('name')
    project_description = data.get('project_description')

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pods WHERE id = %s", (pod_id,))
        existing_pod = cur.fetchone()

        if not existing_pod:
            return jsonify({"error": "Pod not found."}), 404
        
        cur.execute("UPDATE pods SET name = %s, project_description = %s WHERE id = %s", 
                    (name, project_description, pod_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Pod updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
