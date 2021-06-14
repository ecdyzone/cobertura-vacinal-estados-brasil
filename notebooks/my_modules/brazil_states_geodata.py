# dados geo

import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import geobr.read_state
# o método .to_parquet() do geopandas dispara um aviso de cautela para uso em produção
# vamos ocultar este aviso
import warnings
warnings.filterwarnings('ignore', message='.*initial implementation of Parquet.*')

def get_states_geodata():
    path = '../data/geospatial/'
    file = 'geo_estados_2019.parquet.gz'
    filepath = path + file
    
    import os.path
    if os.path.exists(filepath):
        # abreviacoes: gdf para geodataframe, gpd para geopandas
        gdf = gpd.read_parquet(filepath)

    else:
        # a biblioteca geobr, do IPEA, traz dados do ibge em um geodataframe
        gdf = geobr.read_state(code_state='all', year=2019)
        
        # salvando o arquivo no formato parquet, para evitar downloads futuros desnecessarios
        gdf.to_parquet(filepath, compression='gzip')

    # renomeando unidades da federação de acordo com outros dataframes
    renaming_ufs = {'Amazônas': 'Amazonas',
                    'Rio Grande Do Norte': 'Rio Grande do Norte',
                    'Rio De Janeiro': 'Rio de Janeiro',
                    'Rio Grande Do Sul': 'Rio Grande do Sul',
                    'Mato Grosso Do Sul': 'Mato Grosso do Sul'}
    
    # ajustando nomes de colunas
    gdf['name_state'].replace(renaming_ufs, inplace=True)  
    gdf.set_index('name_state', inplace=True)
    gdf.rename_axis('uf', axis=0, inplace=True)
    
    new_columns=['codigo_estado', 'sigla', 'codigo_regiao', 'nome_regiao', 'geometry']
    gdf.rename(columns=dict(zip(gdf.columns, new_columns)), inplace=True)
    
    # convertendo do float64 para int64
    for col in ['codigo_estado', 'codigo_regiao']:
        gdf[col] = gdf[col].astype('int64')
    
    return gdf



def geo_colors_plot(estados_geo: gpd.GeoDataFrame, colors, ax):
    estados_geo['to_plot'] = estados_geo['codigo_estado'].astype(str) + estados_geo['sigla'] + ' - ' + estados_geo.index

    #fig, ax = plt.subplots(figsize=(10,10))#, dpi=300)
    estados_geo.reset_index()

#     colors = colormaps['States']
    # colors = create_ordered_colormap(index=estados_regioes_ordem_oficial.keys(), output_as_list=False, replace_state_color_by_region=True)
    estados_geo.reset_index().plot(column='to_plot', edgecolor='0.3', linewidth=0.4, categorical=True,
                                   legend=True, cmap=colors, ax=ax,
                    legend_kwds={'loc':'center left', 'bbox_to_anchor':(0.9,0.5)})

    for txt in ax.get_legend().get_texts():
        txt.set_text(txt.get_text()[2:])

    ax.set_title('Padrão de Cores por Regiões e Estados', fontsize=20)
    ax.axis('off')

    estados_geo.drop(columns='to_plot', inplace=True)

    # Add Labels in centroids on geomap
#    estados_geo['coords'] = estados_geo['geometry'].apply(lambda x: x.representative_point().coords[:])
#    estados_geo['coords'] = [coords[0] for coords in merged['coords']]for idx, row in estados_geo.iterrows():
#        plt.annotate(s=row['sigla'], xy=row['coords'],horizontalalignment='center')

estados_geo = get_states_geodata()
estados_regioes_ordem_oficial = estados_geo['nome_regiao'].to_dict()

### use example
#fig, ax = plt.subplots(figsize=(10,10))#, dpi=300)
#geo_colors_plot(estados_geo, brazil_colormaps['States'], ax=ax)
