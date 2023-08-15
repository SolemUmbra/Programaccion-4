from flask import Flask, render_template, request

import redis

app = Flask(__name__)

# Connect to the Redis server
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list', methods=['GET'])
def list_words():
    palabras = redis_client.keys('*')
    word_list = []
    for palabra_id in palabras:
        palabra = redis_client.hgetall(palabra_id)
        word_list.append({
            'id': palabra_id.decode(),
            'palabra': palabra[b'PALABRA'].decode(),
            'definicion': palabra[b'DEFINICION'].decode()
        })
    return render_template('list.html', word_list=word_list)

@app.route('/add', methods=['GET', 'POST'])
def add_word():
    if request.method == 'POST':
        palabra = request.form['palabra']
        definicion = request.form['definicion']
        palabra_id = redis_client.incr('next_id')
        nueva_palabra = {
            b'PALABRA': palabra.encode(),
            b'DEFINICION': definicion.encode()
        }
        try:
            redis_client.hmset(palabra_id, nueva_palabra)
            success_message = "Palabra y Definicion agregada con éxito"
        except:
            success_message = "ERR::Palabra y Definicion ya existente, intentar otro"
        return render_template('add.html', success_message=success_message)
    return render_template('add.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit_word():
    if request.method == 'POST':
        palabra_id = int(request.form['id'])
        nueva_palabra = request.form['palabra']
        nueva_definicion = request.form['definicion']
        updated_palabra = {
            b'PALABRA': nueva_palabra.encode(),
            b'DEFINICION': nueva_definicion.encode()
        }
        redis_client.hmset(palabra_id, updated_palabra)
        success_message = "Palabra y Definicion modificada con éxito"
        return render_template('edit.html', success_message=success_message)
    
    palabras = redis_client.keys('*')
    word_list = []
    for palabra_id in palabras:
        palabra = redis_client.hgetall(palabra_id)
        word_list.append({
            'id': palabra_id.decode(),
            'palabra': palabra[b'PALABRA'].decode(),
        })
    return render_template('edit.html', word_list=word_list)

@app.route('/delete', methods=['GET', 'POST'])
def delete_word():
    if request.method == 'POST':
        palabra_id = int(request.form['id'])
        if not redis_client.exists(palabra_id):
            error_message = "ERR::Palabra y Definicion no existe"
        else:
            redis_client.delete(palabra_id)
            success_message = "Palabra y Definicion eliminada con éxito"
        return render_template('delete.html', success_message=success_message, error_message=error_message)
    
    palabras = redis_client.keys('*')
    word_list = []
    for palabra_id in palabras:
        palabra = redis_client.hgetall(palabra_id)
        word_list.append({
            'id': palabra_id.decode(),
            'palabra': palabra[b'PALABRA'].decode(),
            'definicion': palabra[b'DEFINICION'].decode()
        })
    return render_template('delete.html', word_list=word_list)

if __name__ == '__main__':
    app.run(debug=True)
