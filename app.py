import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv('fdr_20261029_132558.csv',sep=',',header=1)
st.title("BlackBox G3X Reader")
st.set_page_config(layout='wide',page_icon='flight')
st.markdown('Utilize A Barra Lateral Para Navegação')

## Sidebar
st.sidebar.title('Menu Interativo')
incidente_acidente=st.sidebar.selectbox(options=['Acidente','Incidente','Outros'],label="Escolha Abaixo",)
if incidente_acidente is None:
   ''
if incidente_acidente is not None :
    red_line=st.sidebar.toggle('Mostra a Perda de Tracao',)
if incidente_acidente == 'Outros':
   red_line= None


if incidente_acidente== "Acidente":
 df_filtered = df[df['UTC Date (yyyy-mm-dd)']=='2026-10-19']
 voo_ocorrencia=df_filtered[df_filtered['UTC Time (hh:mm:ss)']>='13:48:16']
 momento='14:02:28'
 decolagem='14:00:42'


 
if incidente_acidente== 'Incidente':
 df_filtered = df[df['UTC Date (yyyy-mm-dd)']=='2026-10-01']
 # voo_ocorrencia=df_filtered[df_filtered['UTC Time (hh:mm:ss)']>='13:48:16']
 voo_ocorrencia=df_filtered
 momento='14:58:09'
 decolagem='14:57:34'

if incidente_acidente =='Outros':
   day=st.sidebar.select_slider(label='Escolha a Data',options=df['UTC Date (yyyy-mm-dd)'])
#    st.write(day)
   df_filtered_day=df[df['UTC Date (yyyy-mm-dd)']== day]
#    st.write(df)

   voo_ocorrencia=df_filtered_day
   momento=''
print(df.columns)

colu1,colu2,colu3,colu4=st.columns(4,gap='medium')

with colu1 :
    # st.metric('Pressao de Combustivel Max',voo_ocorrencia['Fuel Press (PSI)'].max(),border=True)
    st.metric('Pressao de Combustivel Min',f'{voo_ocorrencia['Fuel Press (PSI)'].min():.0f} PSI',border=False,delta= voo_ocorrencia['Fuel Press (PSI)'].max() - voo_ocorrencia['Fuel Press (PSI)'].min() )

    ''
with colu2:
    st.metric('Pressao Oleo Minima',f'{voo_ocorrencia['Oil Press (PSI)'].min():.0f} PSI',border=False,delta= voo_ocorrencia['Oil Press (PSI)'].min() - voo_ocorrencia['Oil Press (PSI)'].max())
    # st.metric('Pressao Oleo Min',voo_ocorrencia['Oil Press (PSI)'].min(),border=True)
with colu3:
    st.metric('Altitude Maxima',f'{voo_ocorrencia['Baro Altitude (ft)'].max():.0f} Ft',border=False)
with colu4:
    st.metric('Velocidade Maxima',f'{voo_ocorrencia['Indicated Airspeed (kt)'].max():.0f} IAS',border=False,)


## Graficos 
#Figura que mostra o manifold
fig_manifold=go.Figure()
fig_manifold.add_traces(go.Line(x=voo_ocorrencia['UTC Time (hh:mm:ss)'], 
                                y=voo_ocorrencia['Manifold Press (inch Hg)'],
 mode='lines',
 name='Manifold',
 # hovertext=voo_ocorrencia['Manifold Press (inch Hg)'],
 # hoverinfo='none'
 )).update_layout(title='Linha do Tempo Manifold',
                  hovermode='x',
 yaxis=dict(
 title='Manifold em In',
 ),
 xaxis=dict(
 title='Tempo em Horário Z',
 visible=True

 )
 )

fig_rpm=go.Figure()
fig_rpm.add_traces(
 go.Line(
 x=voo_ocorrencia['UTC Time (hh:mm:ss)'],
 y=voo_ocorrencia['RPM'],
 text=voo_ocorrencia['RPM']
 )
 ).add_vline(
 x='14:02:28',
 line_width=1,
 line_dash="dash",
 line_color="red"
 ).add_vline(
 x='14:05:12',
 line_width=1,
 line_dash="dash",
 line_color="yellow"
 ).update_layout(title='Linha do Tempo RPM',
                 xaxis=dict(
                visible=False

                 ))




#figura que compara os CHTS
fig = go.Figure()
fig.add_trace(
 go.Scatter(
 x= voo_ocorrencia['UTC Time (hh:mm:ss)'],
 y=voo_ocorrencia['CHT1 Temp (deg F)'],
 mode='lines',
 name='CHT 1',)).add_trace(
 go.Scatter(
 x= voo_ocorrencia['UTC Time (hh:mm:ss)'],
 y=voo_ocorrencia['CHT2 Temp (deg F)'],
 mode='lines',
 name='CHT 2',
text=voo_ocorrencia['CHT3 Temp (deg F)'],
 )).add_trace(
 go.Scatter(
 x= voo_ocorrencia['UTC Time (hh:mm:ss)'],
 y=voo_ocorrencia['CHT3 Temp (deg F)'],
 mode='lines',
 name='CHT 3',
text=voo_ocorrencia['CHT4 Temp (deg F)'],
 )).add_trace(
 go.Scatter(
 x= voo_ocorrencia['UTC Time (hh:mm:ss)'],
 y=voo_ocorrencia['CHT4 Temp (deg F)'],
 mode='lines',
 name='CHT 4',
text=voo_ocorrencia['CHT4 Temp (deg F)'],
 )).update_layout(
 title='Comparação Entre CHT 1 e CHT 4 Na Ocorrência',
 yaxis=dict(
 title='Temperatura em Fº',
 ),
 xaxis=dict(
 title='Tempo em Horário Z',
 visible=False
 ),
 ).update_traces(showlegend=False)

fig_altitude=go.Figure()
fig_altitude.add_trace(go.Scatter
                (x=voo_ocorrencia['UTC Time (hh:mm:ss)'],
                y=voo_ocorrencia['Baro Altitude (ft)'],
                mode='lines'
              )
              ).update_layout(
                title='Altitude',
                xaxis=dict(
                 title='Linha do Tempo Horario Z',
                 visible=False),
                 yaxis=dict(
                   title='Altitude em FT'
                 )
              )

fig_speed=go.Figure()
fig_speed.add_trace(go.Scatter(
  x=voo_ocorrencia['UTC Time (hh:mm:ss)'],
  y=voo_ocorrencia['Indicated Airspeed (kt)'],
)
).update_layout(
  title='Velocidade Indicada',
  xaxis=dict(
     visible=False
  )

)

if red_line ==True:
  fig_manifold.add_vline(
   x=momento,
   line_width=3,
   line_dash="dash",
   line_color="red",
   label=dict(
   text='Perda de Tração',
   ))
  fig_speed.add_vline(
     x=momento,
       line_width=3,
       line_dash="dash",
       line_color="red",
       label=dict(
       text='Perda de Tração',
       )
  )
  fig.add_vline(
        x=momento,
           line_width=3,
           line_dash="dash",
           line_color="red",
           label=dict(
           text='Perda de Tração',
           )
  )
  fig_speed.add_vline(

        x=momento,
           line_width=3,
           line_dash="dash",
           line_color="red",
           label=dict(
           text='Perda de Tração',
           ),yaxis=dict(
              title='Velocidade IAS'
           )
  )
  fig_altitude.add_vline(
        x=momento,
           line_width=3,
           line_dash="dash",
           line_color="red",
           label=dict(
           text='Perda de Tração',
           )
  )

  

#####

st.subheader('Graficos Interativos')
# print(red_line)
col1,col2=st.columns(2,gap='medium')
with col1 :
  st.plotly_chart(fig_manifold)
  st.plotly_chart(fig_speed)

#  st.plotly_chart(fig_rpm)
with col2:
    st.plotly_chart(fig)
    st.plotly_chart(fig_altitude)
#    st.write('Figura Base de Comparar')
value=st.selectbox('Selecione o Parametro Para Comparacao',options=(df.columns))
fig_generic = go.Figure()
fig_generic.add_trace(
go.Scatter(
x= voo_ocorrencia['UTC Time (hh:mm:ss)'],
y=voo_ocorrencia[value],
mode='lines',
name='CHT 1',)).update_layout(
title=f'Valores  de {value}',
yaxis=dict(
title=' ',
),
xaxis=dict(
title='Tempo em Horário Z',
visible=False
),
).update_traces(showlegend=False)
st.plotly_chart(fig_generic)
voo_mapa = voo_ocorrencia.copy()

# Converter coordenadas para valores numéricos
voo_mapa['Latitude (WGS84 deg)'] = pd.to_numeric(
    voo_mapa['Latitude (WGS84 deg)'], errors='coerce'
)

voo_mapa['Longitude (WGS84 deg)'] = pd.to_numeric(
    voo_mapa['Longitude (WGS84 deg)'], errors='coerce'
)

# Remover coordenadas nulas
voo_mapa = voo_mapa.dropna(
    subset=['Latitude (WGS84 deg)', 'Longitude (WGS84 deg)']
)

# Validar limites geográficos
voo_mapa = voo_mapa[
    voo_mapa['Latitude (WGS84 deg)'].between(-90, 90) &
    voo_mapa['Longitude (WGS84 deg)'].between(-180, 180)
]

st.map(
    voo_mapa,
    latitude='Latitude (WGS84 deg)',
    longitude='Longitude (WGS84 deg)'
)
    # st.text('Fica Evidente Que a Variação do CHT é apenas Falha de Sensor')
