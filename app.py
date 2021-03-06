from flask import Flask, render_template, request
import docker
from .container import Container
import json
from json2html import json2html

app = Flask(__name__)
client = docker.from_env()


@app.route('/')
def index():
    cns = client.containers.list(all=True)
    return render_template('container_list.html', containers=cns)


@app.route('/container/<container>')
def container_details(container):
    entity_type = 'container'
    container_id = container.split(':')[1].strip()[:-1]
    container = client.containers.get(container_id)
    container_logs = container.logs().decode('utf-8').split('\n')
    container_inspect_data = json2html.convert(json=json.dumps(container.attrs), table_attributes='class="table table-sm table-bordered"')
    container_image_inspect_data = json2html.convert(json=json.dumps(container.image.attrs), table_attributes='class="table table-sm table-bordered"')
    return render_template('container.html', container=container, entity=entity_type, container_logs=container_logs, container_inspect_data=container_inspect_data, container_image_inspect_data=container_image_inspect_data)


@app.route('/images')
def images():
    imagelist = client.images.list()
    return render_template('images.html', images=imagelist)


@app.route('/image/<image>')
def image_details(image):
    entity_type = 'image'
    return render_template('image.html', image=image, entity=entity_type)

@app.route('/services')
def service_list():
    print("Service Page")
    servicelist = client.services.list()
    return render_template('service.html', services = servicelist)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
