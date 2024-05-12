from bd import BD
from prettytable import PrettyTable

def calcular_estimativa(BD, generos_desejados):
    # Calcula as ocorrências para cada filme com base nos graus desejados
    for filme in BD:
            filme["OCORRENCIAS"] = 0
            filme["PERCENTUAL"] = 0
            if all(genero in filme["GENERO"] for genero in generos_desejados):
                filme["OCORRENCIAS"] = sum(filme["GENERO"][genero] * generos_desejados[genero] for genero in generos_desejados)
    
    # Calcula o total de ocorrências para normalizar os percentuais
    total_ocorrencias = sum(filme["OCORRENCIAS"] for filme in BD)
    
    # Calcula os percentuais para cada filme
    for filme in BD:
        if total_ocorrencias > 0:
            filme["PERCENTUAL"] = (filme["OCORRENCIAS"] / total_ocorrencias) * 100
    
    # Ordena os filmes com base nos percentuais
    filmes_sem_zero = [filme for filme in BD if filme["PERCENTUAL"] != 0]
    filmes_ordenados = sorted(filmes_sem_zero, key=lambda x: x["PERCENTUAL"], reverse=True)
    
    return filmes_ordenados

# Percorre o banco de dados e retorna todos os gêneros existentes
def listar_generos_em_BD(BD):
    generos_registrados = set()
    for filme in BD:
        for genero in filme["GENERO"]:
            generos_registrados.add(genero)
    return list(generos_registrados)

def main():
    # Faz com que a saída occora apenas quando o usuário quiser encerrar o programa
    sair = False
    while not sair:
        print("SISTEMA ESPECIALISTA DE FILMES")
        # Valida se a entrada das opções são válidas
        while True:
            try:
                sair = True if int(input("Fazer pesquisa - 1\nSair - 0\nSua escolha: ")) == 0 else False
                break
            except ValueError:
                            print("O valor deve ser 1 ou 0")
        # Valida se a opão não foi sair
        if not sair:
            generos_desejados = {}
            
            # Retorna todos os gêneros listados no banco de dados
            generos_existentes = listar_generos_em_BD(BD)
            
            # Guarda as informaçôes de quanto o usuário quer de cada item
            for item in generos_existentes: 
                # Tratando erro para que usuário não insira valor inválidos
                while True:
                        try:
                            valor = int(input(f"Quanto você deseja o gênero {item} no seu filme (ou digite 0 para não adicionar): "))
                            if valor > 0:
                                generos_desejados[item] = valor
                            break 
                        except ValueError:
                            print("O valor deve ser inteiro, tente novamente")

            # Chama a função que calcula baseado nos gêneros escolhidos
            filmes_recomendados = calcular_estimativa(BD, generos_desejados)
            
            # Percorre o vetor de files e mostra os dados em forma de tabela
            if len(filmes_recomendados) > 0:
                for filme in filmes_recomendados:
                    if filme["OCORRENCIAS"] > 0:
                        tabela = PrettyTable()
                        tabela.field_names = [f"{filme['FILME']}", f"{filme['PERCENTUAL']:.0f}%"]
                        generos_ordenados = sorted(filme["GENERO"].items(), key=lambda x: x[1], reverse=True)
                        
                        for genero, peso in generos_ordenados:
                            tabela.add_row([f"Gênero - {genero}", peso])

                        tabela.align = "l"
                        print(tabela)

            # Caso não seja encontrado nenhum resultado devolve ao usuário uma resposta
            else:
                print("perdão, não temos regisrado nenhum filme com todos esses gêneros simultaneamente!")

if __name__ == "__main__":
    main()