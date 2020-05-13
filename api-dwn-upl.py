import os

from flask import Flask, request, abort, jsonify, send_from_directory


UPLOAD_DIRECTORY = "g:/OneDrive/coding/python/PythonPractice/testfolder/api_uploaded_files"
print(os.getcwd()) # Show work dir

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


app = Flask(__name__)


@app.route("/files")   # Endpoint to list files on the server
def listFiles():   

    files = []

    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


#@api.route("/createfile/<text>", methods=["GET"])
#def createFile(text):
#    file = open("testfile.txt", "w")
#    text = input("Enter your text:")
#    file.write(text) 
#    file.close()
#    return jsonify("File created")

@app.route("/files/<path:path>")
def getFile(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@app.route("/files/<filename>", methods=["POST"]) # Upload File
def postFile(filename):
    if "/" in filename:  # Return 400 BAD REQUEST
        abort(400, "No SubDir's Allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    return jsonify(201, 'File uploaded successfully!') # Return 201 CREATED


if __name__ == "__main__":
    app.run(debug=True, port=8000)