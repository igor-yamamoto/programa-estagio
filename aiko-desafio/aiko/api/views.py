"""Arquivo onde sao definidas as views (métodos) para acesso dos dados
contidos nas tabelas. Eles sao distribuidos dentre os 4 metodos pedido
pelo desafio (POST, GET, PUT e DELETE), além de um adicional para
inserção de dados em campos sem ter que atualizar toda a instância
(PATCH).
Os métodos definidos aqui são:

    - operate_list: método que suporta operações de POST, GET e DELETE
        para TODAS as instâncias de um dado modelo. Dentre os modelos:
        Veiculos, Linha, Paradas, PosicaoVeiculos.

    - operate_details: método que suporta operacoes de PUT, GET, PATCH
        e DELETE sobre uma instância de um dado modelo quando fornecido
        o id (pk). Os modelos são os mesmos para o caso da `operate_list`.

    - linhas_por_parada_list: método que suporta apenas a operação GET.
        Ela retorna a lista de todas as paradas, apresentando nelas também
        uma lista contento todas as linhas associadas as paradas.

    - linhas_por_parada_detail: método que suporta as operacoes GET, PUT
        e PATCH. Retorna, quando fornecido o id de uma parada, a instância
        de uma parada, contendo também uma lista com as linhas associadas.

    - veiculos_por_linha_list: método que suporta apenas operações GET.
        Retorna a lista de todas as linhas, apresentando nelas também
        uma lista de todos os veiculos associados a cada linha.

    - veiculos_por_linha_detail: método que suporta as operações GET, PUT
        e PATCH. Retorna, quando fornecido o id de uma linha, a instância
        da linha, contendo também uma lista com os veiculos associados.

    - paradas_por_posicao: método que suporta apenas a operação GET.
        Retorna as três paradas mais próximas da latitude e longitude
        fornecidas como entrada.

    - paradas_por_posicao_n: método que suporta apenas a operacao GET.
        Retorna as N paradas mais próximas da latitude e longitude
        fornecidas como entrada.

"""

from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import api_view

from .serializers import (VeiculoSerializer, LinhaSerializer,
                          ParadasSerializer, PosicaoVeiculosSerializer,
                          LinhasParadaSerializer, VeiculosLinhaSerializer)
from .models import Veiculo, Linha, Paradas, PosicaoVeiculos

from .funcs import get_idx, calculate_distance

models = [Veiculo, Linha, Paradas, PosicaoVeiculos]
serializers = [VeiculoSerializer, LinhaSerializer, ParadasSerializer, PosicaoVeiculosSerializer]
name_models = ['name_veiculo', 'name_linha', 'name_parada']

@api_view(['GET', 'POST', 'DELETE'])
def operate_list(request, modelo):
    """Método para apresentar uma lista dos modelos suportados
    (Paradas, Linhas, Veiculos e PosicaoVeiculos). Aqui, o campo
    "modelo" deve ser preenchido com:
        - veiculos: acesso à lista de veiculos registrados
        - linhas: acesso à lista de linhas registradas
        - paradas: acesso à lista de paradas registradas
        - posicaoveiculos: acesso à lista de posição dos veiculos
    """

    i = get_idx(modelo)

    if i == -1:
        return JsonResponse(
            {'message': 'url não existe dentro da API. Favor, inserir uma dentre as urls possíveis',
             'urls': {'Veiculos': '/api/veiculos/',
                      'Linhas': '/api/linhas/',
                      'Paradas': '/api/paradas/',
                      'Posicao dos veiculos': '/api/posicaoveiculos/',
                      'Relacao de linhas por parada': '/api/paradaslinhas/',
                      'Relacao de veiculos por linhas':'/api/linhasveiculos/',
                      'Posicao das paradas proximas': '/api/paradasposicao/'}
            })

    model = models[i]
    serializer = serializers[i]

    if request.method == 'GET':
        instance = model.objects.all()
        if i in [3]:
            instance_serializer = serializer(instance, many=True)
        else:
            name_model = name_models[i]
            name_instance = request.GET.get(name_model, None)

            if name_instance is not None:
                instance = instance.filter(name_instance__icontains=name_instance)

        instance_serializer = serializer(instance, many=True)
        return JsonResponse(instance_serializer.data, safe=False)

    if request.method == 'POST':
        instance_data = JSONParser().parse(request)
        instance_serializer = serializer(data=instance_data)

        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        instance = model.objects.all()
        instance.delete()
        return JsonResponse({'message': 'Instância excluida'},
                            status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def operate_details(request, modelo, primary_key):
    """Método apra apresentar uma instância de cada modelo suportado
    (Paradas, Linhas, Veiculos e PosicaoVeiculos). Aqui, o campo
    "modelo" deve ser preenchido com:
        - veiculos: acesso à lista de veiculos registrados
        - linhas: acesso à lista de linhas registradas
        - paradas: acesso à lista de paradas registradas
        - posicaoveiculos: acesso à lista de posição dos veiculos

    """

    i = get_idx(modelo)

    if i == -1:
        return JsonResponse(
            {'message': 'url não existe dentro da API. Favor, inserir uma dentre as urls possiveis',
             'urls': {'Veiculos': '/api/veiculos/id:{}'.format(primary_key),
                      'Linhas': '/api/linhas/id:{}'.format(primary_key),
                      'Paradas': '/api/paradas/id:{}'.format(primary_key),
                      'Posicao dos veiculos': '/api/posicaoveiculos/id:{}'.format(primary_key),
                      'Relacao de linhas por parada': '/api/paradaslinhas/id:{}'.format(primary_key),
                      'Relacao de veiculos por linhas':'/api/linhasveiculos/id:{}'.format(primary_key)}
            })

    model = models[i]
    serializer = serializers[i]

    try:
        instance = model.objects.get(pk=primary_key)
    except model.DoesNotExist:
        return JsonResponse({'message': 'Instância nao existe'})

    if request.method == 'GET':
        instance_serializer = serializer(instance)
        return JsonResponse(instance_serializer.data)

    if (request.method == 'PUT' or request.method == 'PATCH'):
        instance_data = JSONParser().parse(request)
        if request.method == 'PUT':
            instance_serializer = serializer(instance, data=instance_data)
        elif request.method == 'PATCH':
            instance_serializer = serializer(instance, data=instance_data, partial=True)
        if instance_serializer.is_valid():
            instance_serializer.save()
            return JsonResponse(instance_serializer.data)
        return JsonResponse(instance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        instance.delete()
        return JsonResponse({'message': 'Instância deletada da base de dados'},
                            status=status.HTTP_204_NO_CONTENT, safe=False)

@api_view(['GET'])
def linhas_por_parada_list(request):
    """Método para listar todas as paradas, acompanhadas das linhas
    associadas."""

    parada_linha = Paradas.objects.all()

    parada_linha_serializer = LinhasParadaSerializer(parada_linha, many=True)
    return JsonResponse(parada_linha_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH'])
def linhas_por_parada_detail(request, parada_id):
    """Método para apresentar uma parada em específico, apresentando
    também as linhas associadas."""

    try:
        parada_linha = Paradas.objects.filter(id=parada_id)
    except models.DoesNotExist:
        return JsonResponse({'message': 'Parada não existe'})

    if request.method == 'GET':
        parada_linha_serializer = LinhasParadaSerializer(parada_linha, many=True)
        return JsonResponse(parada_linha_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        parada_linha = Paradas.objects.get(id=parada_id)
        parada_linha_data = JSONParser().parse(request)
        if request.method == 'PUT':
            parada_linha_serializer = LinhasParadaSerializer(parada_linha,
                                                             data=parada_linha_data)
        elif request.method == 'PATCH':
            parada_linha_serializer = LinhasParadaSerializer(
                parada_linha, data=parada_linha_data, partial=True)

        if parada_linha_serializer.is_valid():
            parada_linha_serializer.save()
            return JsonResponse(parada_linha_serializer.data)
        return JsonResponse(parada_linha_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def veiculos_por_linha_list(request):
    """Método para listar todas as linhas, acompanhadas dos veiculos
    associados."""

    linha_veiculo = Linha.objects.all()

    linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, many=True)
    return JsonResponse(linha_veiculo_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'PATCH'])
def veiculos_por_linha_detail(request, linha_id):
    """Método para apresentar uma linha em específico, apresentando
    também os veiculos associados."""

    try:
        linha_veiculo = Linha.objects.filter(id=linha_id)
    except models.DoesNotExist:
        return JsonResponse({'message': 'Linha não existe'})

    if request.method == 'GET':
        linha_veiculo_serializer = VeiculosLinhaSerializer(linha_veiculo, many=True)
        return JsonResponse(linha_veiculo_serializer.data, safe=False, status=status.HTTP_200_OK)

    elif (request.method == 'PUT' or request.method == 'PATCH'):
        linha_veiculo = Linha.objects.get(id=linha_id)
        linha_veiculo_data = JSONParser().parse(request)
        if request.method == 'PUT':
            linha_veiculo_serializer = VeiculosLinhaSerializer(
                linha_veiculo, data=linha_veiculo_data)
        elif request.method == 'PATCH':
            linha_veiculo_serializer = VeiculosLinhaSerializer(
                linha_veiculo, data=linha_veiculo_data, partial=True)

        if linha_veiculo_serializer.is_valid():
            linha_veiculo_serializer.save()
            return JsonResponse(linha_veiculo_serializer.data)
        return JsonResponse(linha_veiculo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def paradas_por_posicao(request, lat, lon):
    """Método que retorna as três paradas mais próximas, dadas as
    latitudes e longitudes."""

    lat, lon = int(lat), int(lon)
    print(lat)

    paradas = Paradas.objects.all()

    ids, distances = calculate_distance(paradas, lat, lon)

    paradas = Paradas.objects.filter(id__in=ids)

    paradas_posicao_serializer = ParadasSerializer(paradas, many=True)

    return JsonResponse(paradas_posicao_serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def paradas_por_posicao_n(request, lat, lon, n_paradas):
    """Método que retorna as N paradas mais próximas, dada a
    latitude e longitude."""

    paradas = Paradas.objects.all()

    ids, distances = calculate_distance(paradas, lat, lon, n_paradas)

    paradas = Paradas.objects.filter(id__in=ids)

    paradas_posicao_serializer = ParadasSerializer(paradas, many=True)

    return JsonResponse(paradas_posicao_serializer.data, safe=False, status=status.HTTP_200_OK)
