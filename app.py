import os
import sys
from flask import Flask, Response, request, abort, send_from_directory
from flask import render_template
from PIL import Image
from io import StringIO

app = Flask(__name__)

WIDTH = 160
HEIGHT = 120
WORKING_DIR = sys.argv[1]


@app.route('/<path:filename>')
def image(filename):
    try:
        w = int(request.args['w'])
        h = int(request.args['h'])
    except (KeyError, ValueError):
        return send_from_directory('.', filename)

    try:
        im = Image.open(filename)
        im.thumbnail((w, h), Image.ANTIALIAS)
        io = StringIO.StringIO()
        im.save(io, format='JPEG')
        return Response(io.getvalue(), mimetype='image/jpeg')

    except IOError:
        abort(404)

    return send_from_directory(WORKING_DIR, filename)

@app.route('/')
def index():
    images = []
    for root, dirs, files in os.walk('.'):
        files.sort()
        for filename in [os.path.join(root, name) for name in files]:
            if not filename.endswith('.png'):
                continue
            im = Image.open(filename)
            w, h = im.size
            aspect = 1.0*w/h
            print(filename)
            if aspect > 1.0*WIDTH/HEIGHT:
                width = min(w, WIDTH)
                height = width/aspect
            else:
                height = min(h, HEIGHT)
                width = height*aspect
            images.append({
                'width': int(width),
                'height': int(height),
                'src': filename
            })
    return render_template('index.html', images=images)    


# run the application
if __name__ == "__main__":  
    app.run(debug=True)
