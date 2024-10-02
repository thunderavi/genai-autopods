from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Helpforu@09'
app.config['MYSQL_DB'] = 'autopods_db'  # Replace with your actual database name

mysql = MySQL(app)

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

if __name__ == '__main__':
    app.run(debug=True)
