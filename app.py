from flask import Flask, render_template, request
import docker
from .container import Container

app = Flask(__name__)
client = docker.from_env()


@app.route('/')
def index():
    cns = client.containers.list()
    return render_template('container_list.html', containers=cns)


@app.route('/container/<container>')
def container_details(container):
    entity_type = 'container'
    print(type(container))
    print(container)
    container_id = container.split(':')[1].strip()[:-1]
    print(container_id)
    container = client.containers.get(container_id)
    return render_template('container.html', container=container, entity=entity_type)


@app.route('/images')
def images():
    imagelist = client.images.list()
    return render_template('images.html', images=imagelist)


@app.route('/image/<image>')
def image_details(image):
    entity_type = 'image'
    return render_template('image.html', image=image, entity=entity_type)


def service_list():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
