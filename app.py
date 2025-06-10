
import os
from dotenv import load_dotenv 
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify 
import dicionario_data
from google import generativeai as genai


load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24) 

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("\n" + "="*50)
    print("ERRO CRÍTICO: A variável de ambiente GOOGLE_API_KEY NÃO foi carregada.")
    print("Por favor, verifique se você tem um arquivo .env na raiz do projeto")
    print("com o conteúdo: GOOGLE_API_KEY=\"SUA_CHAVE_REAL_AQUI\"")
    print("E se o `pip install python-dotenv` foi executado com sucesso.")
    print("="*50 + "\n")
else:
    print("\n" + "="*50)
    print("DEBUG: API Key do Gemini carregada com sucesso.")
    print("="*50 + "\n")



genai.configure(api_key=API_KEY)

try:
   model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    print(f"ERRO: Não foi possível inicializar o modelo Gemini. Problema com a API Key? {e}")
    model = None 


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}



@app.route('/')
def index():
   
    return render_template('index.html')

@app.route('/about')
def about():
    
    return render_template('about.html')



@app.route('/fundamentos/selecao')
def fundamentos_selecao():
    
    return render_template('fundamentos_selecao.html')

@app.route('/fundamentos/repeticao')
def fundamentos_repeticao():
    
    return render_template('fundamentos_repeticao.html')

@app.route('/fundamentos/vetores')
def fundamentos_vetores():
   
    return render_template('fundamentos_vetores.html')

@app.route('/fundamentos/funcoes')
def fundamentos_funcoes():
   
    return render_template('fundamentos_funcoes.html')

@app.route('/fundamentos/excecoes')
def fundamentos_excecoes():
    
    return render_template('fundamentos_excecoes.html')



@app.route('/dicionario')
def dicionario_listar():
    
    termos = dicionario_data.carregar_dicionario()
    termos_ordenados = sorted(termos.items()) 
    return render_template('dicionario_listar.html', termos=termos_ordenados)

@app.route('/dicionario/adicionar', methods=['GET', 'POST'])
def dicionario_adicionar():
    
    if request.method == 'POST':
        termo = request.form['termo'].strip()
        definicao = request.form['definicao'].strip()

        if not termo or not definicao:
            flash('Erro: Termo e definição não podem ser vazios.', 'danger')
        elif dicionario_data.adicionar_termo(termo, definicao):
            flash(f'Termo "{termo}" adicionado com sucesso!', 'success')
            return redirect(url_for('dicionario_listar'))
        else:
            flash(f'Erro: O termo "{termo}" já existe no dicionário.', 'danger')
    return render_template('dicionario_adicionar.html')

@app.route('/dicionario/alterar/<termo_chave>', methods=['GET', 'POST'])
def dicionario_alterar(termo_chave):
    
    termo_obj = dicionario_data.obter_termo(termo_chave) 
    if not termo_obj:
        flash(f'Erro: Termo "{termo_chave}" não encontrado.', 'danger')
        return redirect(url_for('dicionario_listar'))

    if request.method == 'POST':
        novo_termo = request.form['novo_termo'].strip()
        nova_definicao = request.form['nova_definicao'].strip()

        if not novo_termo or not nova_definicao:
            flash('Erro: Novo termo e nova definição não podem ser vazios.', 'danger')
        elif dicionario_data.atualizar_termo(termo_obj['termo'], novo_termo, nova_definicao):
            flash(f'Termo "{termo_obj["termo"]}" atualizado para "{novo_termo}" com sucesso!', 'success')
            return redirect(url_for('dicionario_listar'))
        else:
            flash(f'Erro: O novo termo "{novo_termo}" já existe (se for diferente do original) ou houve um problema na atualização.', 'danger')
    
    
    return render_template('dicionario_alterar.html', termo=termo_obj['termo'], definicao=termo_obj['definicao'])


@app.route('/dicionario/excluir/<termo_chave>', methods=['POST'])
def dicionario_excluir(termo_chave):
    
    if dicionario_data.excluir_termo(termo_chave):
        flash(f'Termo "{termo_chave}" excluído com sucesso!', 'success')
    else:
        flash(f'Erro: Termo "{termo_chave}" não encontrado para exclusão.', 'danger')
    return redirect(url_for('dicionario_listar'))



@app.route('/gemini_chat', methods=['GET', 'POST']) 
def gemini_chat():
    
    if request.method == 'GET':
        
        return render_template('gemini_chat.html')
    elif request.method == 'POST':
        
        
        if not request.is_json:
            return jsonify({'error': 'A requisição deve ser JSON'}), 400

        data = request.get_json()
        pergunta = data.get('question', '').strip()

        if not pergunta:
            return jsonify({'error': 'Por favor, digite sua pergunta.'}), 400

        
        if not model:
            return jsonify({'error': 'O serviço Gemini não está disponível devido a um problema de configuração da API.'}), 500

        try:
            response = model.generate_content(pergunta)
            resposta = response.text
            
            return jsonify({'answer': resposta}), 200
        except Exception as e:
            print(f"Erro ao gerar conteúdo com Gemini: {e}") 
           
            return jsonify({'error': f"Desculpe, ocorreu um erro ao se comunicar com a IA: {e}"}), 500


if __name__ == '__main__':
    
    dicionario_data._garantir_arquivo_dicionario()
    app.run(debug=True) 