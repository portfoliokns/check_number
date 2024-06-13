from bottle import route, run, template, request
from ai import judge

@route('/')
def view():
    return template('template_view', output_text="")

@route('/', method='POST')
def get_number():
    input_image = request.files.input_image
    output_text = judge(input_image)
    return template('template_view', output_text=output_text)

run(host='localhost', port=8080, debug=True)
