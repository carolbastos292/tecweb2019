from Angelica import app, bcrypt
from flask_jwt import jwt_required
from flask import request, jsonify

from Angelica.models import (
    Usuario,
    Motorista,
    Taxi,
    Permissao
)

from Angelica.schemas import (
    AuthSchema,
    GetUserSchema,
    UserSchema,
    RegisterUserSchema,
    TaxiSchema,
    TaxiInfoSchema,
    TaxiPlacaSchema
)

from Angelica.responses import (
    resp_already_exists,
    resp_refused_credentials,
    resp_exception,
    resp_data_invalid,
    resp_not_exist,
    resp_ok
)

from Angelica.messages import (
    MSG_NO_DATA,
    MSG_INVALID_DATA,
    MSG_RESOURCE_FIND,
    MSG_USER_AUTH
)
from Angelica.messages import (
    MSG_RESOURCE_CREATED,
    MSG_DOES_NOT_EXIST
)

from Angelica.methods import mensagem_feedback
from flask_jwt import jwt_required

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update

import os


@app.route('/')
def index():

    app_name = os.getenv("APP_NAME")

    if app_name:
        return "Hello World running in a Docker container behind Nginx!"

    return 'Hello World!'


def identidade(payload):

    cpf = payload["usuario"]["cpf"] if "usuario" in payload else None
    return Usuario().read(cpf)


@app.route('/auth', methods=['POST'])
def auth():
    """
    Método de autenticação
    Recebe um objeto do tipo JSON com chaves cpf e senha
    Exemplo:
    --------
    {
      'cpf': '88844455522',
      'senha': 'acb1234'
    }
    """

    req_data = request.get_json()
    data, errors = None, None

    if req_data is None:
        return resp_data_invalid('auth', [], msg=MSG_NO_DATA)

    schema = AuthSchema()
    data, errors = schema.load(req_data)

    if errors:
        return resp_data_invalid('auth', errors)
    else:
        try:
            usuario = Usuario().auth(cpf=data['cpf'], senha=data['senha'])

        except Exception as e:
            return resp_exception('auth', description=e)

    if usuario:
        return resp_ok('auth', MSG_USER_AUTH.format(data['cpf']),  data=usuario,)
    else:
        return resp_refused_credentials('auth', [])


@app.route('/admin/create', methods=['POST'])
# @jwt_required()
def create_admin():

    req_data = request.get_json()
    cpf = req_data['cpf']

    if(cpf):
        usuario = Usuario().read(cpf)
        if(not usuario):
            senha = req_data['senha']
            if(senha):
                senha_hash = bcrypt.generate_password_hash(
                    senha).decode("utf-8")
                nome = req_data['nome']
                if(nome):
                    usuario = {
                        "cpf": cpf,
                        "nome": nome,
                        "senha": senha_hash,
                        "status": 1,
                    }
                    usuario = Usuario(usuario)
                    return mensagem_feedback(True, "Usuário cadastrado com sucesso!")
                else:
                    return mensagem_feedback(False, "Nome não pode estar em branco!")
            else:
                return mensagem_feedback(False, "Senha não pode estar em branco!")
        else:
            return mensagem_feedback(False, "CPF já cadastrado na base de dados!")
    return mensagem_feedback(False, "Não foi possível cadastrar o Usuário!")


@app.route('/user', methods=['POST'])
# @jwt_required()
def get_user():
    """
    Método retirna um usuário existente
    Recebe um objeto do tipo JSON com chaves cpf
    Exemplo:
    --------
    {
      'cpf': '88844455522'
    }
    """

    req_data = request.get_json()
    data, errors, result = None, None, None

    if req_data is None:
        return resp_data_invalid('usuario', [], msg=MSG_NO_DATA)

    schema = GetUserSchema()
    data, errors = schema.load(req_data)

    if errors:
        return resp_data_invalid('usuario', errors)

    try:
        model = Usuario().query.get(data)

    except Exception as e:
        return resp_exception('user', description=e)

    if not model:
        return resp_not_exist('user', data['cpf'])

    schema = UserSchema()
    result = schema.dump(model)

    return resp_ok('user', MSG_RESOURCE_FIND.format('Usuário'),  data=result.data,)


@app.route('/users', methods=['GET'])
# @jwt_required()
def get_users():

    try:
        model = Usuario().query.all()

    except Exception as e:
        return resp_exception('user', description=e)

    schema = UserSchema(many=True)
    result = schema.dump(model)

    return resp_ok('users', MSG_RESOURCE_FIND.format('Usuários'),  data=result.data,)


@app.route('/user/register', methods=['POST'])
# @jwt_required()
def register_user():
    """
    Método para cração de um usuário
    Recebe um objeto do tipo JSON com chaves cpf, nome, senha e status
    Exemplo:
    --------
    {
      'cpf': '88844455522',
      'nome': 'Richardson Souza'
      'senha': 'acb1234',
      'status': 1
    }
    """

    req_data = request.get_json()
    data, errors, result = None, None, None

    if req_data is None:
        return resp_data_invalid('user', [], msg=MSG_NO_DATA)
    
    schema = RegisterUserSchema()
    data, errors = schema.load(req_data)

    if errors:
        return resp_data_invalid('user', errors)

    try:
        data['senha'] = bcrypt.generate_password_hash(req_data['senha']).decode("utf-8")
        model = Usuario(data)

    except IntegrityError:
        return resp_already_exists('user', data['cpf'])

    except Exception as e:
        return resp_exception('user', description=e)

    schema = UserSchema()
    result = schema.dump(model)

    return resp_ok(
        'user', MSG_RESOURCE_CREATED.format('Usuário'),  data=result.data,
    )


@app.route('/usuario/update', methods=['POST'])
# @jwt_required()
def update_usuario():

    #cpf = request.form["cpf"] if "cpf" in request.form else None
    req_data = request.get_json()
    cpf = req_data['cpf']

    if(cpf):

        #senha = request.form["senha"] if request.form["senha"] else None
        senha = req_data['senha']
        if(senha):
            senha_hash = bcrypt.generate_password_hash(senha).decode("utf-8")
            nome = req_data['nome']
            if(nome):
                status = req_data['status']
                if(status):

                    usuario = {
                        "cpf": cpf,
                        "nome": nome,
                        "senha": senha_hash,
                        "status": status,
                    }

                    usuario = Usuario().update(usuario)

                    return mensagem_feedback(True, "Usuário atualizado com sucesso!")
                else:
                    return mensagem_feedback(False, "Status faltando!")
            else:
                return mensagem_feedback(False, "Nome fatando!")
        else:
            return mensagem_feedback(False, "Senha fatando!")
    return mensagem_feedback(False, "É necessário informar um CPF")


@app.route('/usuario/delete', methods=['POST'])
# @jwt_required()
def delete_usuario():

    #cpf = request.form["cpf"] if "cpf" in request.form else None
    req_data = request.get_json()
    cpf = req_data['cpf']

    if(cpf):

        usuario = Usuario().delete(cpf)

        return mensagem_feedback(True, "Usuário desativado com sucesso!")

    return mensagem_feedback(False, "É necessário informar um CPF")


'''
    CRUD - Motorista
'''


@app.route('/motorista/get', methods=['POST'])
# @jwt_required()
def get_motorista():

    req_data = request.get_json()
    cpf = req_data['cpf']

    if(cpf):

        motorista = Motorista().read(cpf)

        if(motorista != {}):
            return jsonify(motorista)

        return mensagem_feedback(False, "Motorista não encontrado na base de dados")

    return mensagem_feedback(False, "É necessário informar um CPF")


@app.route('/motoristas/get', methods=['GET'])
# @jwt_required()
def get_motoristas():
    motoristas = Motorista().list()

    return jsonify(motoristas)


@app.route('/motorista/create', methods=['POST'])
# @jwt_required()
def create_motorista():
    req_data = request.get_json()
    cpf = req_data['cpf']

    if(cpf):
        motorista = Motorista().read(cpf)
        if(not motorista):
            if(req_data['rg'] and req_data['nome'] and req_data['renach'] and req_data['telefone'] and req_data['cep'] and req_data['rua'] and req_data['bairro']):
                motorista = {
                    'cpf': cpf,
                    'rg': req_data['rg'],
                    'nome': req_data['nome'],
                    'renach': req_data['renach'],
                    'telefone': req_data['telefone'],
                    'cep': req_data['cep'],
                    'rua': req_data['rua'],
                    'bairro': req_data['bairro'],
                    'status': 1,
                }
                motorista = Motorista(motorista)
                return mensagem_feedback(True, "Motorista cadastrado com sucesso!")
            else:
                return mensagem_feedback(False, "Preencha todos os campos.")
        else:
            return mensagem_feedback(False, "CPF já cadastrado na base de dados!")

    return mensagem_feedback(False, "Não foi possível cadastrar o Motorista.")


@app.route('/motorista/update', methods=['POST'])
# @jwt_required()
def update_motorista():
    req_data = request.get_json()
    cpf = req_data['cpf']

    if(cpf):
        if(req_data['rg'] and req_data['nome'] and req_data['renach'] and req_data['telefone'] and req_data['cep'] and req_data['rua'] and req_data['bairro'] and req_data['status']):
            motorista = {
                'cpf': cpf,
                'rg': req_data['rg'],
                'nome': req_data['nome'],
                'renach': req_data['renach'],
                'telefone': req_data['telefone'],
                'cep': req_data['cep'],
                'rua': req_data['rua'],
                'bairro': req_data['bairro'],
                'status': req_data['status']
            }
            motorista = Motorista().update(motorista)
            return mensagem_feedback(True, "Motorista atualizado com sucesso!")
        else:
            return mensagem_feedback(False, "Preencha todos os campos.")

    return mensagem_feedback(False, "É necessário informar um CPF")


@app.route('/motorista/delete', methods=['POST'])
# @jwt_required()
def delete_motorista():
    req_data = request.get_json()
    cpf = req_data['cpf']

    if(cpf):
        motorista = Motorista().delete(cpf)
        return mensagem_feedback(True, "Motorista desativado com sucesso!")

    return mensagem_feedback(False, "É necessário informar um CPF")


'''
    CRUD - Taxi
'''


@app.route('/taxi/get', methods=['POST'])
# @jwt_required()
def get_taxi():

    req_data = request.get_json()
    data, errors, result = None, None, None

    if req_data is None:
        return resp_data_invalid('Taxi', [], msg=MSG_NO_DATA)

    schema = TaxiPlacaSchema()
    data, errors = schema.load(req_data)

    if errors:
        return resp_data_invalid('Taxi', errors)

    try:
        model = Taxi().query.get(data)

    except Exception as e:
        return resp_exception('Taxi', description=e)

    if not model:
        return resp_not_exist('Taxi', data['placa'])

    schema = TaxiInfoSchema()
    result = schema.dump(model)

    return resp_ok('Taxi', MSG_RESOURCE_FIND.format('Taxi'),  data=result.data,)


@app.route('/taxis/get', methods=['GET'])
# @jwt_required()
def get_taxis():

    try:
        model = Taxi().query.all()

    except Exception as e:
        return resp_exception('Taxi', description=e)

    schema = TaxiInfoSchema(many=True)
    result = schema.dump(model)

    return resp_ok('Taxi', MSG_RESOURCE_FIND.format('Taxi'),  data=result.data,)


@app.route('/taxi/create', methods=['POST'])
# @jwt_required()
def create_taxi():

    req_data = request.get_json()
    data, errors, result = None, None, None
    schema = TaxiSchema()

    if req_data is None:
        return resp_data_invalid('Taxi', [], msg=MSG_NO_DATA)

    data, errors = schema.load(req_data)

    if errors:
        return resp_data_invalid('Taxi', errors)

    try:
        model = Taxi(data)

    except IntegrityError:
        return resp_already_exists('Taxi', data['placa'])

    except Exception as e:
        return resp_exception('Taxi', description=e)

    schema = TaxiSchema()
    result = schema.dump(model)

    # Retorno 200
    return resp_ok(
        'Taxi', MSG_RESOURCE_CREATED.format('Taxi'),  data=result.data,
    )


@app.route('/taxi/update', methods=['POST'])
# @jwt_required()
def update_taxi():

    req_data = request.get_json()
    data, errors, result = None, None, None

    if req_data is None:
        return resp_data_invalid('Taxi', [], msg=MSG_NO_DATA)

    schema = TaxiInfoSchema()
    data, errors = schema.load(req_data)

    print(data)

    if errors:
        return resp_data_invalid('Taxi', errors)

    try:
        taxi = Taxi().query.get(data['placa'])
        #data, errors = schema.load(data, instance=Taxi().query.get(data['placa']), partial=True)
        #model = Taxi().update().where(placa==data['placa']).values(data)

    except Taxi.DoesNotExist:
        return resp_not_exist('Taxi', data['placa'])

    except Exception as e:
        return resp_exception('Taxi', description=e)

    print(taxi)

    update_query = taxi.update(data)
    update_query.execute()
    result = schema.dump(taxi)

    # Retorno 200
    return resp_ok(
        'Taxi', MSG_RESOURCE_CREATED.format('Taxi'),  data=data,
    )


@app.route('/taxi/delete', methods=['POST'])
@jwt_required()
def delete_taxi():

    placa = request.form["placa"] if "placa" in request.form else None

    if(placa):

        motorista = Taxi().delete(placa)

        return mensagem_feedback(True, "Taxi desativado com sucesso!")

    return mensagem_feedback(False, "É necessário informar uma placa")


'''
    CRUD - Permissão
'''


@app.route('/permissao/get', methods=['POST'])
@jwt_required()
def get_permissao():

    motorista = request.form["motorista"] if "motorista" in request.form else None
    usuario = request.form["usuario"] if "usuario" in request.form else None
    taxi = request.form["taxi"] if "taxi" in request.form else None

    if(taxi and usuario and motorista):
        permissao = Permissao().read(taxi, motorista, usuario)

        if(permissao != {}):
            return jsonify(permissao)

        return mensagem_feedback(False, "Permissão não encontrada na base de dados")

    return mensagem_feedback(False, "Faltam informações necessárias")


@app.route('/permissoes/get', methods=['GET'])
@jwt_required()
def get_permissoes():
    permissoes = Permissao().list()

    return jsonify(permissoes)


@app.route('/permissao/create', methods=['POST'])
@jwt_required()
def create_permissao():

    motorista = request.form["motorista"] if "motorista" in request.form else None
    usuario = request.form["usuario"] if "usuario" in request.form else None
    taxi = request.form["taxi"] if "taxi" in request.form else None

    # Substituir True por função de verificar se já foi cadastrado.
    if(taxi and usuario and motorista and True):

        permissao = {
            "taxi": taxi,
            "motorista": motorista,
            "usuario": usuario,
            "inicio": request.form["nome"] if "nome" in request.form else "Não informado",
            "fim": request.form["nome"] if "nome" in request.form else "Não informado",
            "tipo": request.form["nome"] if "nome" in request.form else "Não informado",
            "status": request.form["status"] if "status" in request.form else 1,
        }

        permissao = Permissao(permissao)

        return mensagem_feedback(True, "Permissão cadastrada com sucesso!")

    elif(taxi and usuario and motorista and True):
        return mensagem_feedback(False, "Dados já cadastrados na base de dados!")

    return mensagem_feedback(False, "Não foi possível cadastrar a Permissão!")


@app.route('/permissao/update', methods=['POST'])
@jwt_required()
def update_permissao():

    motorista = request.form["motorista"] if "motorista" in request.form else None
    usuario = request.form["usuario"] if "usuario" in request.form else None
    taxi = request.form["taxi"] if "taxi" in request.form else None

    if(taxi and usuario and motorista):

        permissao = {
            "taxi": taxi,
            "motorista": motorista,
            "usuario": usuario,
            "data_inicio": request.form["data_inicio"] if "data_inicio" in request.form else "Não informado",
            "data_fim": request.form["data_fim"] if "data_fim" in request.form else "Não informado",
            "tipo": request.form["tipo"] if "tipo" in request.form else "Não informado",
            "status": request.form["status"] if "status" in request.form else 1,
        }

        permissao = Permissao().update(permissao)

        return mensagem_feedback(True, "Permissão atualizada com sucesso!")

    return mensagem_feedback(False, "Dados insuficientes para atualização")


@app.route('/permissao/delete', methods=['POST'])
@jwt_required()
def delete_permissao():

    motorista = request.form["motorista"] if "motorista" in request.form else None
    usuario = request.form["usuario"] if "usuario" in request.form else None
    taxi = request.form["taxi"] if "taxi" in request.form else None

    if(taxi and usuario and motorista):

        permissao = Permissao().delete(taxi, motorista, usuario)

        return mensagem_feedback(True, "Permissão desativado com sucesso!")

    return mensagem_feedback(False, "Dados insuficientes para exclusão")


@app.route('/info/taxi', methods=['POST'])
def info_taxi():
    pass
