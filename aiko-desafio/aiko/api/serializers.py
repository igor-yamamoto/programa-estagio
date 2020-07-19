"""Arquivo contendo os serializadores a serem implementados na API.
Alguns deles possuem a versão simplificada, que é para serem passa-
dos a outros serializadores, com o objetivo de nao apresentar redun
dância na serialização dos dados (os mesmos dados poderem ser acessa
dos em diversos url's diferentes). Os campos marcados com asterisco
(*) sao listas.

Dentro deles:

    - ParadasSerializer:
        Modelo: Parada
        Campos: id, nome da parada, latitude, longitude

    - LinhaSerializer:
        Modelo: Linha
        Campos: id, nome da linha, paradas associadas*

    - LinhaSimplesSerializer:
        Modelo: Linha
        Campos: id, nome da linha

    - VeiculoSerializer:
        Modelo: Veiculo
        Campos: id, nome do veiculo, modelo do veiculo, id da linha,
            posicao*
        Serializadores externos: PosicaoVeiculosSimplesSerializer

    - VeiculoSimplesSerializer:
        Modelo: Veiculo
        Campos: id, nome do veiculo, modelo do veiculo

    - PosicaoVeiculoSerializer:
        Modelo: PosicaoVeiculo
        Campos: latitude do veiculo, longitude do veiculo, id do
            veiculo

    - PosicaoVeiculoSimplesSerializer:
        Modelo: PosicaoVeiculos
        Campos: latitude do veiculo, longitude do veiculo

    - LinhasParadaSerializer:
        Modelo: Paradas
        Campos: id, nome da parada, latitude, longitude, linhas*
        Serializadores externos: LinhaSimplesSerializer

    - VeiculosLinhaSerializer:
        Modelo: Linha
        Campos: id, nome da linha, paradas*, veiculos*
        Serializadores externos: VeiculoSimplesSerializer

"""

from rest_framework import serializers
from .models import Veiculo, Linha, Paradas, PosicaoVeiculos

class PosicaoVeiculosSerializer(serializers.ModelSerializer):
    """Serializador da posição dos veiculos."""

    veiculo_id = serializers.IntegerField()

    class Meta:
        """Classe Meta para o serializador de PosicaoVeiculos."""

        model = PosicaoVeiculos
        fields = ['lat_veiculo', 'long_veiculo', 'veiculo_id']

class PosicaoVeiculosSimplesSerializer(serializers.ModelSerializer):
    """Serializador simplificado da posição dos veiculos."""

    class Meta:
        """Classe Meta para o serializador simplificado de
        PosicaoVeiculos."""

        model = PosicaoVeiculos
        fields = ['lat_veiculo', 'long_veiculo']

class VeiculoSerializer(serializers.ModelSerializer):
    """Serializador dos veiculos."""

    linha_id = serializers.IntegerField()
    posicao = PosicaoVeiculosSimplesSerializer(read_only=True)

    class Meta:
        """Classe Meta para o serializador de Veiculo."""

        model = Veiculo
        fields = ['id', 'name_veiculo', 'model_veiculo', 'linha_id', 'posicao']
        extra_kwargs = {'posicao': {'required': False}}

class VeiculoSimplesSerializer(serializers.ModelSerializer):
    """Serializador simplificado dos veiculos."""

    class Meta:
        """Classe Meta para o serializador simplificado de
        Veiculo."""

        ordering = ['id']
        model = Veiculo
        fields = ['id', 'name_veiculo', 'model_veiculo']

class VeiculosLinhaSerializer(serializers.ModelSerializer):
    """Serializador da relação de veiculos por linhas."""

    veiculos = VeiculoSimplesSerializer(many=True, read_only=True)

    class Meta:
        """Classe Meta para o serializador da relacao de
        veiculos por linha."""

        ordering = ['id']
        model = Linha
        fields = ['id', 'name_linha', 'paradas', 'veiculos']
        extra_kwargs = {'paradas': {'required': False}}
        extra_kwargs = {'veiculos': {'required': False}}

class LinhaSerializer(serializers.ModelSerializer):
    """Serializador das linhas."""

    class Meta:
        """Classe Meta para o serializador de Linha."""

        ordering = ['id']
        model = Linha
        fields = ['id', 'name_linha', 'paradas']
        extra_kwargs = {'paradas': {'required': False}}

class LinhaSimplesSerializer(serializers.ModelSerializer):
    """Serializador simplificado das linhas."""

    class Meta:
        """Classe Meta para o serializador simplificado de
        Linha."""

        ordering = ['id']
        model = Linha
        fields = ['id', 'name_linha']

class ParadasSerializer(serializers.ModelSerializer):
    """Serializador das paradas."""

    class Meta:
        """Classe Meta para o serializador de Paradas."""

        ordering = ['id']
        model = Paradas
        fields = ['id', 'name_parada', 'lat_parada', 'long_parada']

class LinhasParadaSerializer(serializers.ModelSerializer):
    """Serializador da relação de linhas por paradas."""

    linhas = LinhaSimplesSerializer(many=True, read_only=True)

    class Meta:
        """Classe Meta para o serializador da relação de linhas
        por paradas."""

        ordering = ['id']
        model = Paradas
        fields = ['id', 'name_parada', 'lat_parada', 'long_parada', 'linhas']
        extra_kwargs = {'linhas': {'required': False}}
