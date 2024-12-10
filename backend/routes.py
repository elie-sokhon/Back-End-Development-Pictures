from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    urls=[]
    for picture in data:
        urls.append(picture["pic_url"])
    return jsonify(urls)
        

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return jsonify({
                "id":picture["id"],
                "pic_url":picture["pic_url"]
            })
    abort(404, description="Picture not found")


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()
    if not new_picture or "id" not in new_picture:
        return {"Message":"Invalid parameter"},422
    for picture in data:
        if picture["id"] == new_picture["id"]:
            return {"Message":f"picture with id {picture['id']} already present"},302
        
    data.append(new_picture)
    return {"Message": "Picture successfully added", "id": new_picture["id"]}, 201

    

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    query = request.get_json()
    
    if not query:
        return {"Message":"Invalid parameter"},422

    for picture in data:
        if picture["id"] == id:
            picture.update(query)
            return {"message": f"Picture with id {id} updated successfully."}, 201
    return {"message":"picture not found"},404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    
    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "",204
    return {"message":"picture not found"},404

