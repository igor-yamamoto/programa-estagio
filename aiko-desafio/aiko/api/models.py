"""Arquivo onde são definidos os modelos (tabelas do banco de dados)
a serem implementados na API."""

from django.db import models

class Paradas(models.Model):
    """Modelo (tabela) para Paradas. Consiste dos campos:
        - nome (CHARFIELD, max_lenght=50)
        - latitude (BIGINT)
        - longitude (BIGINT)."""

    name_parada = models.CharField(max_length=50, blank=False, default='')
    lat_parada = models.BigIntegerField(blank=False)
    long_parada = models.BigIntegerField(blank=False)

    def __str__(self):
        return str(self.name_parada)

class Linha(models.Model):
    """Modelo (tabela) para Linhas. Consiste dos campos:
        - nome (CHARFIELD, max_lenght=50)
        - paradas (FOREIGN KEY - MANY TO MANY). """

    name_linha = models.CharField(max_length=50, blank=False, default='')
    paradas = models.ManyToManyField('Paradas', related_name='linhas', blank=True)

    def __str__(self):
        return str(self.name_linha)

class Veiculo(models.Model):
    """Modelo (tabela) para Veiculos. Consiste dos campos:
        - nome (CHARFIELD, max_length=30)
        - modelo (CHARFIELD, max_length=30)
        - linha (FOREIGN KEY - MANY TO ONE)."""

    name_veiculo = models.CharField(max_length=30, blank=False, default='')
    model_veiculo = models.CharField(max_length=30, blank=False, default='')
    linha = models.ForeignKey('Linha', related_name='veiculos',
                              on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name_veiculo)

class PosicaoVeiculos(models.Model):
    """Modelo (tabela) para PosicaoVeiculos. Consiste dos campos:
        - latitude (BIGINT)
        - longitude (BIGINT)
        - veiculos_id (PRIMARY KEY/FOREIGN KEY - ONE TO ONE)."""

    lat_veiculo = models.BigIntegerField(blank=True)
    long_veiculo = models.BigIntegerField(blank=True)
    veiculo = models.OneToOneField('Veiculo', related_name='posicao',
                                   on_delete=models.CASCADE, primary_key=True)
