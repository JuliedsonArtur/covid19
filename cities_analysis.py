#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 10:20:22 2021

@author: juliedson
"""

# Gera gráficos da pandemia para diversas cidades do Brasil

# import packages
import pandas as pd # dataframes
import matplotlib.pyplot as plt # plotting data
import seaborn as sns

# Inputing the city name
print("\033[1;32m\nOi! A coisa tá difícil, eu sei... \nMas juntos vamos passar por tudo isso!!! :D\033[m"\
      "\n\nEscreva o nome da cidade no seguinte formato:\nCidade/UF",\
      "\nExemplos: Natércia/MG; São Paulo/SP; Pouso Alegre/MG\n")
city = str(input('Nome do município: '))#'Heliodora/MG'#Fazer mecanismo de busca'
city_name = city.replace('/', '_')
print('\n\033[1;37mEntão vamos dar uma olhada em como está \033[1;36m'+str(city.replace('/', ' - '))+'...\033[m')

# Chosing a path to sabe the figs
#wanna_path = str(input('Deseja escolher alguma pasta para salvar? [S/N] ')).upper()[0]
#if wanna_path in 'SY':
#    path = str(input('Digite aqui o caminho: '))
#else:
#    path=''

df_cities = pd.read_csv("https://github.com/wcota/covid19br/blob/master/cases-brazil-cities-time.csv.gz?raw=true", compression='gzip')
df_cities["date"] = pd.to_datetime(df_cities["date"])

df_city = df_cities[df_cities.city == city]

#Taking only last 5 weeks of the data
semanas_5 = df_cities[df_cities.city == city].copy()
semanas_5 = semanas_5[-6*7:]
semanas_5.shape

# Renamng axis into Portuguese
semanas_5["Data"]=semanas_5["date"]
semanas_5["Novos Casos"] = semanas_5["newCases"]#loc[semanas_5["newCases"] != 0]
semanas_5["Novas Mortes"] = semanas_5["newDeaths"]#.loc[semanas_5["newDeaths"] != 0]
semanas_5["Semana Epidemiológica"] = semanas_5["epi_week"]
semanas_5["Novas Mortes (m.m. 7 dias)"] = semanas_5["newDeaths_7d"] = semanas_5["newDeaths"].rolling(7).mean()
semanas_5["Novos Casos (m.m. 7 dias)"] = semanas_5["newCases"].rolling(7).mean()
semanas_5["Data"]=semanas_5["date"]
semanas_5["Casos Acumulados"] = semanas_5["totalCases"]
semanas_5["Mortes Acumuladas"] = semanas_5["deaths"]
semanas_5["Novos Casos (m.m. 7 dias)"] = semanas_5["newCases"].rolling(7).mean()
#
#
#
# Pandemic situation of the last 5 weeks
fig, ax = plt.subplots(sharex=True)
semanas_5.plot(x='Data', y='Novos Casos', ax=ax )
semanas_5.plot(x='Data', y='Novos Casos (m.m. 7 dias)', ax=ax )
semanas_5.plot(x="Data", y="Casos Acumulados", secondary_y=True, ax=ax, linestyle='--')
plt.tight_layout()
plt.title('Pandemia COVID-19 em '+str(city))
#plt.show()
plt.savefig('COVID_19_pandemic_5weeks_'+str(city_name)+'.jpg', dpi=300, bbox_inches='tight', pad_inches=0.4)
#
#
#
# Trend line of new cases last 5 weeks
plt.figure()
sns.regplot(x="Semana Epidemiológica", y="Novos Casos", \
            data=semanas_5, fit_reg=True, label='5 Semanas', line_kws={"ls": "--"})
sns.regplot(x="Semana Epidemiológica", y="Novos Casos (m.m. 7 dias)",\
            data=semanas_5, fit_reg=True, label='5 Semanas (m.m.)', line_kws={"ls": "--"})
plt.title('Linha de Tendência para Novos Casos em '+str(city), fontsize=14)
plt.legend()
plt.tight_layout()
#plt.show()
plt.savefig('tendencia_novos_casos_'+str(city_name)+'.jpg', dpi=300, bbox_inches='tight', pad_inches=0.4)
#
#
#
# Total cases last 5 weeks
plt.figure()
semanas_5["Casos Acumulados"] = semanas_5["totalCases"]#.loc[semanas_5["newCases"] != 0]
sns.regplot(x="Semana Epidemiológica", y="Casos Acumulados", data=semanas_5, line_kws={"ls": "--"})#, fit_reg=True)
plt.title('Casos Acumulados nas últimas semanas - '+str(city), fontsize=12)
plt.tight_layout()
#plt.show()
plt.savefig('tendencia_casos_acumulados_'+str(city_name)+'.jpg', dpi=300, bbox_inches='tight', pad_inches=0.4)
#
#
#
# Copy the data
# Names in Portuguese
_df = df_cities[df_cities.city == city].copy()
_df["Data"]=_df["date"]
_df["Casos Acumulados"] = _df["totalCases"]
_df["Mortes Acumuladas"] = _df["deaths"]
_df["Novos Casos"] = _df["newCases"].loc[_df["newCases"] >= 0]
_df["Novas Mortes"] = _df["newDeaths"].loc[_df["newDeaths"] != 0]
_df["Semana Epidemiológica"] = _df["epi_week"]
_df["Novas Mortes (m.m. 7 dias)"] = _df["newDeaths"].rolling(7).mean()
_df["Novos Casos (m.m. 7 dias)"] = _df["newCases"].rolling(7).mean()
#
#
#
# Pandemic in the city for all time
fig, ax = plt.subplots(sharex=True)
_df.plot(x='Data', y='Novos Casos', ax=ax, lw=1)
_df.plot(x='Data', y='Novos Casos (m.m. 7 dias)', ax=ax, lw=2)
_df.plot(x="Data", y="Casos Acumulados", secondary_y=True, ax=ax, lw=3)
plt.tight_layout()
plt.title('Pandemia COVID-19 em '+str(city))
#plt.show()
plt.savefig('COVID_19_pandemic_'+str(city_name)+'_total.jpg', dpi=300, bbox_inches='tight', pad_inches=0.4)
#
#
#
# Corelation of deaths and number of cases
plt.figure()
sns.lmplot(x='Casos Acumulados', y='Mortes Acumuladas', data=_df, line_kws={"ls": "--", "color": "red"})
plt.title('Correlação Mortes x Casos em '+str(city), fontsize='14')
plt.tight_layout()
#plt.show()
plt.savefig('correlacao_mortes_casos_'+str(city_name)+'.jpg', dpi=200, bbox_inches='tight', pad_inches=0.4)
#
#
#
# Raw number of new deaths and mobile mean (?) - média móvel, gente, não sei traduzir Kkkkk 
plt.figure()
ax = plt.gca()
_df = df_cities[df_cities.city == city].copy()
plt.tight_layout()
_df["Novas Mortes (m.m. 7 dias)"] = _df["newDeaths"].rolling(7).mean()
_df["Novas Mortes"] = _df["newDeaths"].loc[_df["newDeaths"] != 0]
_df["Data"] = _df["date"]
_df.plot(x = "Data", y="Novas Mortes",marker=".",lw=0, ax=ax)
_df.plot(x = "Data", y="Novas Mortes (m.m. 7 dias)",ax=ax,lw=3)
plt.title('Número de Novas Mortes em '+str(city))
#plt.show()
plt.savefig('novas_mortes_'+str(city_name)+'.jpg', dpi=200, bbox_inches='tight', pad_inches=0.4)
#
#
#
# Finishing
print('\033[1;36mTerminei! Agora abre o diretório onde está esse código.\n\n Lave bem as mãos! Deus está conosco!  :D  Vai dar tudo certo!!!\n\n')
