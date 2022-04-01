"""
Universidade Federal de Uberlândia - Campus Monte Carmelo
Faculdade de Computação - Sistemas de Informação
GSI521 - Organização e Recuperação da Informação - Prof. Dr. Murillo G. Carneiro
Phelipe Rodovalho Santos

CODIGO FONTE - Estrutura de busca com modelo vetorial tf-idf
"""

# importando o pacote OS para usar funcionalidades que são dependentes do sistema operacional como navegar entre os diretorios e ler arquivos.
import os
import pprint
import math
import csv
global tf
global df
global tfidf
global idf
idf = {}
tfidf = {}
df = {}
tf = {}


def main():
    # função que lê e preenche as variaveis globais que serão usadas por todo o código
    read_documents()
    # preparando os documentos retirando pontuações e stopwords
    document01 = prepare_doc('doc1_patinho_feio.txt')
    document02 = prepare_doc('doc2_joao_maria.txt')
    document03 = prepare_doc('doc3_pinoquio.txt')
    document04 = prepare_doc('doc4_branca_neve.txt')
    document05 = prepare_doc('doc5_cinderela.txt')

    # ordenando os documentos por ordem alfabetica
    document01.sort()
    document02.sort()
    document03.sort()
    document04.sort()
    document05.sort()

    # criando indice invertido de cada um dos documentos e salvando no dicionario global dict_terms
    criar_indice_invertido(document01, 1)
    criar_indice_invertido(document02, 2)
    criar_indice_invertido(document03, 3)
    criar_indice_invertido(document04, 4)
    criar_indice_invertido(document05, 5)

    # calculando ponderação td-idf de cada termo dos documentos
    peso_tf_idf(document01, 1)
    peso_tf_idf(document02, 2)
    peso_tf_idf(document03, 3)
    peso_tf_idf(document04, 4)
    peso_tf_idf(document05, 5)

    pesquisa = str(input("Informe os termos da pesquisa:"))
    # convertendo para minusculo e separando os termos
    pesquisa = pesquisa.lower().split()

    consulta_modelo_vetorial(pesquisa)


def peso_tf_idf(document, num_d):
    numTermsDocument = len(document)
    for t in document:
        # numero de arquivos que termo aparece
        numFilesAppear = len(set(dict_terms.get(t)))
        idff = (1 + math.log(numFilesAppear) *
                math.log(numTermsDocument/numFilesAppear))
        tfidf.setdefault(t, [])
        tfidf[t].append([num_d, idff])


def consulta_modelo_vetorial(pesquisa):
    docs_pesquisa = []
    for p in pesquisa:  # percorrendo os termos de pesquisa fornecidos pelo usuário
        if dict_terms.get(p) is not None:  # se o termo existir
            # recuperando o numero dos documentos que possuem o termo
            for i in dict_terms.get(p):
                if i not in docs_pesquisa:
                    # inserindo o numero dos documentos de cada termo na lista
                    docs_pesquisa.append(i)

    if len(docs_pesquisa) == 0:  # caso nenhum termo for encontrado nos termos mapeados, encerra
        print("Nenhum termo de pesquisa valido foi encontrado")
        exit()

    sim = []
    dict_pondera = {}
    for p in pesquisa:  # percorrendo os termos de pesquisa fornecidos pelo usuário
        try:
            sim.append(list(tfidf.get(p)))
        except:
            continue

    with open("resultado.txt", "w") as f:
        print("_________ Ponderacao TF-IDF das palavras pesquisadas _________ \n", file=f)
        for p in pesquisa:
            print("\nPalavra: ", p, file=f)
            print(tfidf.get(p), file=f)

    with open("ponderacaotf-idf.txt", "w") as f:
        print("_________ Ponderacao TF-IDF de todo corpus _________ \n", file=f)
        for key, value in tfidf.items():
            print("\nPalavra: ", key, file=f)
            print("Valor: ", value, file=f)

#    with open('ponderacaotf-idf.csv', 'w') as csvfile:
#        fieldnames = list(tfidf.keys())
#        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#        writer.writeheader()
#        writer.writerow(tfidf)


def criar_indice_invertido(document, num):  # criando indice invertido
    for d in document:  # percorrendo o documento
        if d not in dict_terms:
            dict_terms.setdefault(d, [])
            dict_terms[d].append(num)
        # se o termo não esta no dict e não é um termo repetido
        if d in dict_terms and num not in dict_terms[d]:
            dict_terms[d].append(num)


def prepare_doc(file):
    # passando o conteudo de cada arquivo para uma lista de string
    document = str(docs.get(file))
    # convertendo tudo para minusculo e retirando o \n
    document = document.lower().replace("\\n", "")

    for p in punctuation:  # percorrendo o vetor de pontuação
        document = document.replace(p, "")  # retirando a pontuação da string

    # separando no espaço todas as palavras e inserindo em uma lista
    document = document.split()
    # inserindo na lista somente as palavras que NAO constam na lista de stopwords
    document = [d for d in document if not d in stopwords]

    return document


def read_documents():
    # definindo variaveis globais
    global punctuation
    global stopwords
    global dict_terms
    global docs

    path = "collection_docs"  # caminho do diretório que contem a coleção de documentos
    docs = {}  # criando dicionário vazio que irá armazenar o conjunto de documentos
    # criando dicionario vazio que irá armazenas os termos do conjunto de documentos
    dict_terms = {}

    # lendo o arquivo de pontuação
    with open('punctuation.txt', 'r',  encoding="utf8") as f:
        punctuation = f.read()
    # separando todas as pontuações e inserindo em formato de lista em punctuation
    punctuation = punctuation.split()

    # lendo o arquivo de stopwords
    with open('stopwords_ptbr.txt', 'r', encoding="utf8") as f:
        stopwords = f.read()
    # separando todas as stopwords e inserindo em formato de lista em stopwords
    stopwords = stopwords.split("\n")

    # lendo todos os arquivos dentro do diretorio no caminho PATH
    for filename in os.listdir(path):
        # abrindo arquivo com encoding utf8 para receber acentos e caracteres especiais adequadamente
        with open(os.path.join(path, filename), 'r', encoding="utf8") as f:
            # salvando conteudo dos arquivos na lista de documentos
            docs[filename] = f.readlines()


main()
