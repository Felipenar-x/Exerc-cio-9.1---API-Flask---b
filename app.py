from flask import Flask, jsonify, request

app = Flask(__name__)


items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]



@app.route('/')
def hello_world():
    return "<h1>Hello World!</h1><p>A API RESTful está rodando em /items</p>"



@app.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": items})



@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify({"item": item})
    return jsonify({"error": "Item não encontrado"}), 404



@app.route("/items", methods=["POST"])
def create_item():
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Dados inválidos"}), 400

    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": request.json["name"]
    }
    items.append(new_item)
    return jsonify(new_item), 201



@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item não encontrado"}), 404

    item["name"] = request.json.get("name", item["name"])
    return jsonify(item)



@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"result": "Sucesso", "message": f"Item {item_id} removido"})


if __name__ == "__main__":
    app.run(debug=True)