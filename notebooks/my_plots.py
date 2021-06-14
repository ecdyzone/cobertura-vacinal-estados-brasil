import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from mapclassify import classify

def mono_br_geoplot(ano: int, gdf: gpd.GeoDataFrame, df: pd.DataFrame, which_plot=0):

    # ano = 2017
    # gdf = estados_geo
    titles= [f'Unidades Federativas Agrupadas\nPor Quartis ({ano})', f'Unidades Federativas Agrupadas\nPor Intervalos Fixos ({ano})']

    bins=[60, 65, 70, 75, 80]
    schemes = ['quantiles', 'UserDefined']
    cmaps = ['coolwarm_r', "cividis"]
    column= str(ano) + '_cobertura_vacinal'

    data_to_plot = df.query("ano==@ano").groupby(by='uf', sort=False).mean().round(2).cobertura_vacinal

    if gdf.index.equals(data_to_plot.index):
        gdf[column] = data_to_plot
    else: 
        print('Can\'t merge. Indexes are not the same')
        return
    # fig, axs = plt.subplots(1,2,figsize=(10,10), facecolor='0.5')
    fig, ax = plt.subplots(1,1, figsize=(10,10))

    if which_plot==0:
        gdf.plot(
            column=column,
            edgecolor='0.5',
    #         linewidth=.1
            cmap=cmaps[0], 
            scheme = schemes[0],
            k=4,
            legend=True,
            legend_kwds=dict(loc='center right', bbox_to_anchor=(1,0.1), title="Cobertura Vacinal\n", title_fontsize= 'medium'),
            ax=ax)
    else:
        gdf.plot(
            column=column,
            edgecolor='0.5',
            cmap=cmaps[1],
            scheme = schemes[1],
        #     k=4,
            legend=True,
            legend_kwds=dict(loc='center right', bbox_to_anchor=(1,0.1),  title="Cobertura Vacinal\n", title_fontsize= 'medium'),
            ax=ax,
            classification_kwds = dict(bins=bins))

    ## formatting legend
#     for i in range(len(axs.flatten())):
#     iterable = []
    
#     for i in iterable:
#         if axs[i] is not None:
    i = 0
    axs = [ax]
    
    axs[i].set_title(titles[which_plot])
    axs[i].axis('off')

    custom_classifier = classify(y=data_to_plot, scheme=schemes[which_plot], bins=bins*which_plot, k=4+which_plot)

    legend_texts = axs[i].get_legend().texts

    for legend_number in range(len(legend_texts)):
    
        vmin,vmax = legend_texts[legend_number].get_text().split(", ")
        number_of_states_per_class = custom_classifier.counts[legend_number]

        text_to_write = '{:.2f} a {:.2f}%  ({} UFs)'.format(float(vmin), float(vmax), number_of_states_per_class)
        legend_texts[legend_number].set_text(text_to_write)

        if which_plot == 1 :

            text_to_write = f'≤ {bins[0]}%  ({number_of_states_per_class} UFs)' if f'a {bins[0]}.00%' in text_to_write else text_to_write
            text_to_write = f'> {bins[-1]}%  ({number_of_states_per_class} UFs)' if f'{bins[-1]}.00 a' in text_to_write else text_to_write
            text_to_write = text_to_write.replace('.00', '')
            legend_texts[legend_number].set_text(text_to_write)



def double_br_geoplot(ano: int, gdf: gpd.GeoDataFrame, df: pd.DataFrame, save=True):

    # ano = 2017
    # gdf = estados_geo
    titles= ['Unidades Federativas Agrupadas\nPor Quartis', 'Unidades Federativas Agrupadas\nPor Intervalos Fixos']

    bins=[60, 65, 70, 75, 80]
    schemes = ['quantiles', 'UserDefined']
    cmaps = ['coolwarm_r', "cividis"]
    column= str(ano) + '_cobertura_vacinal'

    data_to_plot = df.query("ano==@ano").groupby(by='uf', sort=False).mean().round(2).cobertura_vacinal

    if gdf.index.equals(data_to_plot.index):
        gdf[column] = data_to_plot
    else: 
        print('Can\'t merge. Indexes are not the same')
        return
    # fig, axs = plt.subplots(1,2,figsize=(10,10), facecolor='0.5')
    fig, axs = plt.subplots(1,2, constrained_layout=False ,figsize=(20,10))

    gdf.plot(
        column=column,
        edgecolor='0.5',
#         linewidth=.1
        cmap=cmaps[0], 
        scheme = schemes[0],
        k=4,
        legend=True,
        legend_kwds=dict(loc='center right', bbox_to_anchor=(1,0.1), title="Cobertura Vacinal\n", title_fontsize= 'medium'),
        ax=axs[0])

    gdf.plot(
        column=column,
        edgecolor='0.5',
        cmap=cmaps[1],
        scheme = schemes[1],
    #     k=4,
        legend=True,
        legend_kwds=dict(loc='center right', bbox_to_anchor=(1,0.1), title="Cobertura Vacinal\n", title_fontsize= 'medium'),
        ax=axs[1],
        classification_kwds = dict(bins=bins))

    ## formatting legend
#     for i in range(len(axs.flatten())):
    for i in range(len(axs.flatten())):

        axs[i].set_title(titles[i])
        axs[i].axis('off')

        custom_classifier = classify(y=data_to_plot, scheme=schemes[i], bins=bins*i, k=4+i)
        
        legend_texts = axs[i].get_legend().texts
        for legend_number in range(len(legend_texts)):
            vmin,vmax = legend_texts[legend_number].get_text().split(", ")
            number_of_states_per_class = custom_classifier.counts[legend_number]
            
            text_to_write = '{:.2f} a {:.2f}%  ({} UFs)'.format(float(vmin), float(vmax), number_of_states_per_class)
            legend_texts[legend_number].set_text(text_to_write)
            
            if i ==1 :
                
                text_to_write = f'≤ {bins[0]}%  ({number_of_states_per_class} UFs)' if f'a {bins[0]}.00%' in text_to_write else text_to_write
                text_to_write = f'> {bins[-1]}%  ({number_of_states_per_class} UFs)' if f'{bins[-1]}.00 a' in text_to_write else text_to_write
                text_to_write = text_to_write.replace('.00', '')
                legend_texts[legend_number].set_text(text_to_write)
                
    fig.suptitle(f"{ano}")
    
    if save == True:
        fig.savefig("../reports/figures/cloropleths/geo" + str(ano) + "_to_gif.png", facecolor='w',transparent=None)
        plt.close()
    else: 
        plt.show()
