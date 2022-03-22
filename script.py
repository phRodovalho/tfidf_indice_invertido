"""
Universidade Federal de Uberlândia - Campus Monte Carmelo
Faculdade de Computação - Sistemas de Informação
GSI521 - Organização e Recuperação da Informação - Prof. Dr. Murillo G. Carneiro
Phelipe Rodovalho Santos

CODIGO FONTE - Estrutura de índice invertido baseado no modelo vetorial tf-idf
"""

# importando o pacote OS para usar funcionalidades que são dependentes do sistema operacional como navegar entre os diretorios e ler arquivos.
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import pprint

global tf
tf = {}
global df
df = {}
global idf
idf = {}
global tfidf
tfidf = {}


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
    criar_indice_invertido(document01, '1')
    criar_indice_invertido(document02, '2')
    criar_indice_invertido(document03, '3')
    criar_indice_invertido(document04, '4')
    criar_indice_invertido(document05, '5')

    peso_tf(document01, 1)
    peso_tf(document02, 2)
    peso_tf(document03, 3)
    peso_tf(document04, 4)
    peso_tf(document05, 5)

    peso_df((document01 + document02 + document03 + document04 + document05))

    peso_idf(df, tf, document01, 1)
    peso_idf(df, tf, document02, 2)
    peso_idf(df, tf, document03, 3)
    peso_idf(df, tf, document04, 4)
    peso_idf(df, tf, document05, 5)

    corpus = [str(document01) + str(document02) + str(document03) + str(document04) + str(document05)]
    # assign documents
    d0 = 'geek1'
    d1 = 'geek2'
    d2 = 'geek3'
    d3 = 'geek4'
  
    # merge documents into a single corpus
    string = [d0, d1, d2, d3]
    tfidf_m = TfidfVectorizer()

    result = tfidf_m.fit_transform(corpus)

   

    pesquisa = str(input("Informe os termos da pesquisa:"))
    # convertendo para minusculo e separando os termos
    pesquisa = pesquisa.lower().split()

    consulta_booleana(pesquisa)


def peso_df(documents):

    # df(t) = ocorrencia de t no documento
    for t in documents:
        df[t] = (documents.count(t))


def peso_tf(document, n):

    # tf(t,d) = quantidade de t in document / numero de palavras em d
    for t in document:
        print((document.count(t)))
        print(len(document))
        tf[t, n] = (document.count(t) / len(document))


def peso_idf(df, tf, document, d):

    print(df)
    print(tf)

    for t in document:
        print(tf[t, d])
        print(df[t])
        tfidf[t, d] = (tf[t, d] * df[t])


def consulta_booleana(pesquisa):
    docs_pesquisa = []
    for p in pesquisa:  # percorrendo os termos de pesquisa fornecidos pelo usuário
        if dict_terms.get(p) is not None:  # se o termo existir
            print(p + " : " + dict_terms.get(p))
            aux = dict_terms.get(p)
            aux = aux.split()
            # inserindo o numero dos documentos de cada termo na lista
            docs_pesquisa.append(aux)

    if len(docs_pesquisa) == 0:  # caso nenhum termo for encontrado nos termos mapeados, encerra
        print("Nenhum termo de pesquisa valido foi encontrado")
        exit()

    # convertendo a primeira posição para set
    result_pesquisa = set(docs_pesquisa[0])
    for dc in range(len(docs_pesquisa)):  # percorrendo o tamanho da lista
        # convertendo a lista em set
        docs_pesquisa[dc] = set(docs_pesquisa[dc])
        result_pesquisa = result_pesquisa.intersection(
            docs_pesquisa[dc])  # função de intersecção

    result_pesquisa = sorted(result_pesquisa)
    if(len(result_pesquisa) > 1):
        print("A pesquisa retornou os seguintes documentos: ",
              result_pesquisa)
    elif(len(result_pesquisa) == 1):
        print("A pesquisa retornou o seguinte documento: ",
              result_pesquisa)
    else:
        print("A pesquisa não retornou nenhum documento")


def criar_indice_invertido(document, num):  # criando indice invertido
    for d in document:  # percorrendo o documento
        if d not in dict_terms:
            dict_terms[d] = num
        # se o termo não esta no dict e não é um termo repetido
        if d in dict_terms and num not in dict_terms[d]:
            x = str(dict_terms[d])+" "
            # atualiza a lista de documentos do termo
            dict_terms.update({d: x+num})

    pprint.pprint(dict_terms)
    #with open('Indice_Invertido_termos_mapeados.txt', 'w') as file_name: #
    #    pprint.pprint(dict_terms, file_name)..


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
