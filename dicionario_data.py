# dicionario_data.py
import json
import os

# Define o caminho para a pasta de dados onde o dicionário será armazenado
DATA_FOLDER = 'data'
# Define o caminho completo para o arquivo JSON do dicionário
DICIONARIO_FILE = os.path.join(DATA_FOLDER, 'dicionario.json')

def _garantir_diretorio():
    """
    Função auxiliar para garantir que a pasta 'data' exista.
    Cria o diretório se ele não existir.
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

def _garantir_arquivo_dicionario():
    """
    Função auxiliar para garantir que o arquivo do dicionário exista e esteja formatado corretamente.
    Se o arquivo não existir, ele é criado com um dicionário JSON vazio {}.
    MODIFICADO: Inclui termos padrão se o arquivo for criado pela primeira vez.
    """
    _garantir_diretorio() # Garante que a pasta 'data' exista primeiro
    if not os.path.exists(DICIONARIO_FILE):
        termos_iniciais = {
            "Python": "Linguagem de programação de alto nível, interpretada, de script, imperativa, orientada a objetos, funcional e multiparadigma.",
            "Flask": "Microframework para desenvolvimento web em Python, leve e flexível.",
            "Variável": "Um nome simbólico que aponta para um valor armazenado na memória, que pode ser alterado durante a execução do programa.",
            "Função": "Um bloco de código organizado e reutilizável que é usado para executar uma única ação relacionada, podendo receber argumentos e retornar valores.",
            "Loop": "Estrutura de controle que repete um bloco de código múltiplas vezes, como 'for' e 'while' loops.",
            "Estrutura de Dados": "Maneira particular de organizar e armazenar dados em um computador para que possam ser acessados e modificados eficientemente.",
            "Algoritmo": "Conjunto finito de instruções bem definidas e não ambíguas, que são executadas em uma sequência específica para resolver um problema ou realizar uma tarefa."
        }
        with open(DICIONARIO_FILE, 'w', encoding='utf-8') as f:
            json.dump(termos_iniciais, f, indent=4, ensure_ascii=False)
        print(f"Arquivo '{DICIONARIO_FILE}' criado com termos iniciais.")
    else:
        print(f"Arquivo '{DICIONARIO_FILE}' já existe.")


def carregar_dicionario():
    """
    Carrega os termos e definições do arquivo JSON.
    Retorna um dicionário Python com os dados.
    """
    _garantir_arquivo_dicionario() # Garante que o arquivo e o diretório existam antes de ler
    with open(DICIONARIO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dicionario(dicionario):
    """
    Salva o dicionário Python atual no arquivo JSON.
    O arquivo é formatado com indentação para melhor legibilidade.
    """
    _garantir_arquivo_dicionario() # Garante que o arquivo e o diretório existam antes de escrever
    with open(DICIONARIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(dicionario, f, indent=4, ensure_ascii=False)

def adicionar_termo(termo, definicao):
    """
    Adiciona um novo termo e sua definição ao dicionário.
    A busca por termos existentes é case-insensitive.
    Retorna True se o termo foi adicionado com sucesso, False se o termo já existe.
    """
    dicionario = carregar_dicionario()
    # Verifica se o termo (case-insensitive) já existe
    if termo.lower() in [k.lower() for k in dicionario.keys()]:
        return False # Termo já existe
    dicionario[termo] = definicao # Adiciona o termo (mantém a capitalização original)
    salvar_dicionario(dicionario)
    return True

def obter_termo(termo_chave):
    """
    Retorna um dicionário contendo o termo e sua definição,
    ou None se o termo não for encontrado (busca case-insensitive).
    """
    dicionario = carregar_dicionario()
    # Busca o termo de forma case-insensitive, mas retorna o termo original (case-sensitive)
    for termo, definicao in dicionario.items():
        if termo.lower() == termo_chave.lower():
            return {"termo": termo, "definicao": definicao}
    return None

def atualizar_termo(termo_antigo, novo_termo, nova_definicao):
    """
    Atualiza um termo existente no dicionário.
    Permite alterar tanto o termo em si quanto sua definição.
    Retorna True se atualizado, False se o termo antigo não foi encontrado ou se o novo termo já existe (e é diferente do antigo).
    """
    dicionario = carregar_dicionario()
    # Encontra a chave original do termo antigo (case-sensitive)
    original_key = None
    for key in dicionario.keys():
        if key.lower() == termo_antigo.lower():
            original_key = key
            break

    if original_key:
        # Se o novo termo for diferente do original (case-insensitive)
        if original_key.lower() != novo_termo.lower():
            # Verifica se o novo termo já existe no dicionário (excluindo a própria chave original)
            if novo_termo.lower() in [k.lower() for k in dicionario.keys() if k.lower() != original_key.lower()]:
                return False # O novo nome já é usado por outro termo
        
        # Remove a entrada antiga (se o nome do termo mudou ou se for o mesmo termo)
        del dicionario[original_key]
        # Adiciona a nova entrada com o novo termo (se for diferente) e nova definição
        dicionario[novo_termo] = nova_definicao
        salvar_dicionario(dicionario)
        return True
    return False

def excluir_termo(termo_chave):
    """
    Exclui um termo do dicionário.
    A busca por termos para exclusão é case-insensitive.
    Retorna True se o termo foi excluído, False se não foi encontrado.
    """
    dicionario = carregar_dicionario()
    # Encontra a chave original do termo (case-sensitive) para exclusão
    original_key = None
    for key in dicionario.keys():
        if key.lower() == termo_chave.lower():
            original_key = key
            break

    if original_key:
        del dicionario[original_key]
        salvar_dicionario(dicionario)
        return True
    return False