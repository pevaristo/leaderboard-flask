from flask import render_template, url_for, request, make_response, jsonify, redirect
from core import app, dao
from core.models import Match
#from core.leaderboard import Leaderboard
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html',)

@app.route('/contato')
def contato():
    return render_template('contato.html',)

@app.route('/placar')
def placar():
    registros = dao.listar_todos()
    Leaderboard = [p.to_dict() for p in registros]
    return render_template('placar.html', entries=Leaderboard)

@app.route('/placar/add', methods=['GET'])
def placar_add():
    add_match = Match(
          nickname= "paulo",
          score= 99988,
          seconds= 120,
          text= ""
    )
    dao.inserir(add_match)
    return redirect(url_for('placar'))

@app.route('/placar/rm', methods=['GET'])
def placar_rm():
    #leaderboard = Leaderboard
    #leaderboard.pop()
    registros = dao.listar_todos()
    if registros:
        ultimo_registro = registros[-1]
        dao.deletar(ultimo_registro.id)
    return redirect(url_for('placar'))

@app.route('/leaderboard')
def leaderboard():
    registros = dao.listar_todos()
    return make_response(
        jsonify([p.to_dict() for p in registros])
    )


@app.route('/api/leaderboard', methods=['GET', 'POST'])
@app.route('/api/leaderboard/<int:entry_id>', methods=['GET', 'PUT', 'DELETE'])
def admin_leaderboard(entry_id=None):
    
    # GET: Retorna a lista ou um item específico
    if request.method == 'GET':
        if entry_id is not None:
            match = dao.buscar_por_id(entry_id)
            if match:
                return jsonify(match.to_dict()), 200
            return jsonify({"error": "ID inválido"}), 404
            
        registros = dao.listar_todos()
        return jsonify([p.to_dict() for p in registros]), 200

    # POST: Criar nova entrada
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validação Básica
        if not data.get('nickname') or not data.get('score'):
            return jsonify({"error": "Nickname e Score são obrigatórios"}), 400
        
        try:
            # Cria o modelo (a classe base TimestampModel gera o created_at/updated_at em UTC)
            nova_partida = Match(
                nickname=str(data.get('nickname')),
                score=int(data.get('score')),
                seconds=int(data.get('seconds', 0)),
                text=str(data.get('text', ''))
            )
            
            # Insere no banco (o DAO injeta o ID gerado pelo autoincrement no objeto)
            dao.inserir(nova_partida)
            
            if not request.is_json:
                return redirect(url_for('placar'))
                
            return jsonify(nova_partida.to_dict()), 201
            
        except (ValueError, TypeError):
            return jsonify({"error": "Dados inválidos fornecidos"}), 400

    # PUT: Atualizar entrada existente
    if request.method == 'PUT':
        match_existente = dao.buscar_por_id(entry_id) if entry_id is not None else None
        if not match_existente:
            return jsonify({"error": "ID inválido"}), 404
            
        data = request.get_json()

        # Atualiza os campos do objeto mantendo o valor antigo caso não seja enviado no payload
        match_existente.nickname = data.get('nickname', match_existente.nickname)
        match_existente.score = int(data.get('score', match_existente.score))
        match_existente.seconds = int(data.get('seconds', match_existente.seconds))
        match_existente.text = data.get('text', match_existente.text)
        
        # O método dao.atualizar() invoca internamente o registrar_atualizacao() para renovar o updated_at
        dao.atualizar(match_existente)
        return jsonify(match_existente.to_dict()), 200

    # DELETE: Remover entrada
    if request.method == 'DELETE':
        if entry_id is None:
            return jsonify({"error": "ID não fornecido"}), 400
            
        linhas_afetadas = dao.deletar(entry_id)
        if linhas_afetadas > 0:
            return jsonify({"message": "Removido com sucesso"}), 200
            
        return jsonify({"error": "ID inválido"}), 404

@app.route('/placar/admin')
def admin_placar():
    registros = dao.listar_todos()
    Leaderboard = [p.to_dict() for p in registros]
    return render_template('admin_placar.html', entries=Leaderboard)