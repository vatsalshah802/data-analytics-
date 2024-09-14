# import main libraries
import streamlit as st
import numpy as np 
import pandas as pd 
import plotly.express as px 
import io
import time
import statsmodels.api as sm
from scipy import stats
import streamlit as st


# Custom CSS to hide GitHub icon

# set page title and title icon  
st.set_page_config(
    page_title= "Data Analysis Portal ",
    page_icon= '📊'
)
custom_css = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# add title and subheader
st.title (":blue[Data] :red[Operations] :green[Gateway] 🚥")
st.header(":rainbow[Exploratry Data Analysis]", divider = "rainbow")

# step 1 :
st.subheader(":green[Understading Of Data]")

# file uploading & file showing
file = st.file_uploader("Drop csv, excel or json file", type= ["csv", "xlsx","josn"])

if (file!=None):
    if(file.name.endswith("csv")):
        df = pd.read_csv(file)
    elif(file.name.endswith("xlsx")):
        df = pd.read_excel(file)
    elif(file.name.endswith("json")):
        df = pd.read_json(file) 
    with st.spinner('Loading...'):
        time.sleep(3)
    st.dataframe(df)

    st.success("File 📝 is Successfully Uploaded...", icon= "✅")
    
    st.header(":rainbow[Basic Information of this Dataset]", divider = "rainbow")
    tab1,tab2,tab3,tab4,tab5 = st.tabs(['Shape','Top, Bottom & Sample', 
                                             'Information','Describe','Columns'])
     
    with tab1:
        st.write(f'💠 There are {df.shape[0]} rows in this dataset.')
        st.write(f'💠 There are {df.shape[1]} columns in this dataset.')

    with tab2:
        st.subheader(':orange[⬆ Rows : ]')
        st.dataframe(df.head(6))

        st.subheader(':orange[⬇ Rows : ]')
        st.dataframe(df.tail(6))

        st.subheader(':orange[Sample ↕ Rows : ]')
        st.dataframe(df.sample(6))
    
    with tab3:
        st.subheader(':violet[Normal Summary of Data in Dataset.]')
        def display_df_info(df):
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
            return info_str
        info_str = display_df_info(df)
        st.text(info_str)


    with tab4:
        st.subheader(':violet[Statistical Summary of Data in Dataset.]')
        st.dataframe(df.describe())


    with tab5:
        st.subheader(':grey[Columns Name in this Dataset.]')
        st.write(list(df.columns))
    
    
    st.header(':rainbow[Data Cleaning.]', divider='rainbow')
    tab7,tab9 = st.tabs(['Missing Values', 'Duplicate'])

    with tab7:
        subtab1  = st.toggle('Check Missing Values') #'Removing Values', 'filling Values'])
        if subtab1:
            st.subheader(':violet[Total Missing/Null Values in Dataset.]')
            st.write((df.isnull().sum().sum()))
            st.subheader(':violet[Check Missing/Null Values in Dataset.]')
            st.write((df.isnull().sum().sort_values(ascending=False)))
            st.subheader(':violet[Missing/Null values in % of Dataset.]')
            st.write(((df.isnull().sum()/df.shape[0])*100).sort_values(ascending = False))
            st.subheader(':violet[Missing/Null values show by HeatMap in Dataset.]')
            st.warning('Here below show the "While Lines" indicates that there is a Missing/Null within the Dataset.')
            fig = px.imshow(df.isnull())
            st.plotly_chart(fig)

        subtab2 = st.toggle('Removing Values')
        if subtab2:
            tab19,tab20 = st.tabs(['Remove Row Wise','Remove Column Wise'])
            with tab19:
                    st.subheader(':violet[Drop all Missing/Null Values in Dataset.]')
                    clean_df = df.dropna()
                    st.subheader(':violet[Check Drop after Missing/Null values]')
                    st.write((clean_df.isnull().sum().sort_values(ascending=False)))
                    clean = st.button('Clean_Dataframe')
                    st.subheader(':violet[After Missing/Null values show by HeatMap in Dataset.]')
                    fig = px.imshow(clean_df.isnull() )
                    st.plotly_chart(fig)
                    if (clean == True):
                        st.dataframe(clean_df)
                    
            with tab20:
                st.subheader(':violet[Drop Column wise Missing/Null Values in Dataset.]')
                columns = df.columns.tolist()
                #Multi-select widget to choose columns to delete
                columns_to_delete = st.multiselect("Select columns to delete", options=columns)
        
                if st.button("Delete Selected Columns"):
                    #Drop the selected columns
                    df.drop(columns=columns_to_delete, inplace= True)
                    st.write("Updated DataFrame:")
                    st.dataframe(df)
        
                    st.subheader(':violet[Check Missing/Null Values in Dataset.]')
        
         ## Fill missing values in numeric columns with the mean value

        subtab3 = st.toggle('Filling Values')
        if subtab3:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                mean_value = df[col].mean()
                df[col].fillna(mean_value, inplace=True)

        # Fill missing values in categorical columns with the most frequent value
            categorical_cols = df.select_dtypes(include=[object]).columns
            for col in categorical_cols:
                most_frequent_value = df[col].mode()[0]
                df[col].fillna(most_frequent_value, inplace=True)

            st.write("DataFrame after filling missing values:")
            st.write(df)
            st.write((df.isnull().sum().sort_values(ascending=False)))

        

    with tab9:
        st.subheader(':grey[Duplication Check]')
        st.warning('Here below show the "true" value indicates that there is a duplicate value within the dataset.')
        st.write(dict(df.duplicated().value_counts()))
        st.subheader(':orange[Duplicated value in %]')
        dupli_pr = ((df.duplicated().sum()/df.shape[0])*100)
        st.info(f'❗ Percentage of duplicate rows are :orange[{dupli_pr:.2f}] %')
        delete = st.button("Remove Duplicated Rows", type = 'primary')
        if (delete==True):
            df.drop_duplicates(inplace=True)
            st.write("Updated Dataframe :")
            st.write(df)
            st.write(dict(df.duplicated().value_counts()))

    
    st.header(':rainbow[Statistical Analysis.]', divider='rainbow')
    tab15,tab16 = st.tabs(['Descriptive Statistics', 'Frequency Distribution'])
    with tab15:
        from statsmodels.stats.descriptivestats import describe
        st.write(describe(df))
    
    with tab16:
        obj = st.button('Object Describe')
        if (obj == True):
                st.subheader(':violet[Categorical Summary of Data in Dataset.]')
                st.dataframe(df.describe(include= ['O']))

    st.header(':rainbow[Visualizations.]', divider='rainbow')
    with st.expander('Value Counts'):
        col1,col2 = st.columns(2)
        with col1:
            column = st.selectbox("Select columns to graph", options=list(df.columns))
        with col2:  
            row = st.number_input('choose top frequencies', min_value=1, step=1)

        count = st.button('Count')
        if (count == True):
            new_df = df[column].value_counts().reset_index().head(row)
            st.dataframe(new_df)
            fig = px.histogram(data_frame=new_df, x=column,y='count',template='plotly_white',hover_data='count',text_auto='count')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=new_df, names= column, values='count')
            st.plotly_chart(fig)

    st.header(':rainbow[Analytical Visualizations.]', divider='rainbow')
    with st.expander('Group By Data Columns'):
        col3,col4,col5 = st.columns(3)
        with col3:
            secx_col = st.multiselect('Choose Group By Columns', options=list(df.columns))
        with col4:
            secy_col = st.selectbox('Choose Columns for Operations', options=list(df.columns))      
        with col5:
            operation = st.selectbox('Choose One Operation', options=['sum','minimum','maximum','average','mean','median','mode','count','variance','standard deviation'])
        
        if secx_col:
                new_df = df.groupby(secx_col).agg(New_Column = (secy_col,operation)).reset_index()
                st.dataframe(new_df)

                st.subheader(':green[Look 👀 to Data by Graphically]', divider='orange')
                graph = st.selectbox('Choose a Graph Type', options=['line','histogram','barchart','scatterplot','boxplot','violinplot','piechart','sunburst',])
                if graph == 'line':
                    x_axis = st.selectbox('Choose X - Axis Column :', options=list(new_df.columns))
                    y_axis = st.selectbox('Choose Y - Axis Column :', options=list(new_df.columns))
                    color = st.selectbox('Choose Color (Additional Information) :', options = [None] + list(new_df.columns))
                    fig = px.line(data_frame = new_df, x = x_axis, y = y_axis, color = color, markers= 'o', title= f'Line Chart of {x_axis} --> {y_axis}. ')
                    st.plotly_chart(fig)
                
                elif graph == 'histogram':
                    x_axis = st.selectbox('Choose X - Axis Column :', options=list(new_df.columns))
                    y_axis = st.selectbox('Choose Y - Axis Column :', options=list(new_df.columns))
                    color = st.selectbox('Choose Color (Additional Information) :', options = [None] + list(new_df.columns))
                    df_sort = new_df.sort_values(by= 'New_Column', ascending=True)
                    fig = px.histogram(data_frame = df_sort, x = x_axis, y = y_axis,text_auto= 'count',color = color,template='plotly_white', title= f'Histogram of {x_axis} --> {y_axis}.', hover_data = [x_axis,y_axis])
                    st.plotly_chart(fig)
    
                
                elif graph == 'barchart':
                    x_axis = st.selectbox('Choose X - Axis Column :', options=list(new_df.columns))
                    y_axis = st.selectbox('Choose Y - Axis Column :', options=list(new_df.columns))
                    color = st.selectbox('Choose Color (Additional Information) :', options = [None] + list(new_df.columns))
                    facet_col = st.selectbox('Column Information :', options = [None] + list(new_df.columns))
                    fig = px.bar(data_frame = new_df, x = x_axis, y = y_axis,text_auto= 'count', color = color,facet_col= facet_col, title= f'Bar Chart of {x_axis} --> {y_axis}.',hover_data = [x_axis,y_axis])
                    st.plotly_chart(fig)

                elif graph == 'scatterplot':
                    x_axis = st.selectbox('Choose X - Axis Column :', options=list(new_df.columns))
                    y_axis = st.selectbox('Choose Y - Axis Column :', options=list(new_df.columns))
                    color = st.selectbox('Choose Color (Additional Information) :', options = [None] + list(new_df.columns))
                    size = st.selectbox('Size Column : ', options = [None] + list(new_df.columns))
                    fig = px.scatter(data_frame= new_df, x=x_axis, y=y_axis, color=color, size=size, title= f'Scatter Plot of {x_axis} --> {y_axis}.', hover_data= [x_axis,y_axis])
                    st.plotly_chart(fig)

                elif graph == 'boxplot':
                    x_axis = st.selectbox('Choose X - Axis Column :', options=list(new_df.columns))
                    y_axis = st.selectbox('Choose Y - Axis Column :', options=list(new_df.columns))
                    color = st.selectbox('Choose Color (Additional Information) :', options = [None] + list(new_df.columns), title= f'Box Plot of {x_axis} --> {y_axis}.')
                    fig = px.box(data_frame=new_df, y=y_axis, color = color)
                    st.plotly_chart(fig)

                elif graph == 'violinplot':
                    x_axis = st.selectbox('Choose X - Axis Column :', options=list(new_df.columns))
                    y_axis = st.selectbox('Choose Y - Axis Column :', options=list(new_df.columns))
                    color = st.selectbox('Choose Color (Additional Information) :', options = [None] + list(new_df.columns))
                    fig = px.violin(data_frame=new_df, y=y_axis, x = x_axis, color = color, box= True, hover_data=new_df.columns, title= f'Violin Plot of {x_axis} --> {y_axis}.')
                    st.plotly_chart(fig)

                elif graph == 'piechart':
                    x_axis = st.selectbox('Choose X - Axis Column :', options=list(new_df.columns))
                    y_axis = st.selectbox('Choose Y - Axis Column :', options=list(new_df.columns))
                    fig = px.pie(data_frame=new_df, names= x_axis, values=y_axis, title= f'Pie Chart of {x_axis} --> {y_axis}.')
                    st.plotly_chart(fig)

                elif graph == 'sunburst':
                    path = st.multiselect('Choose your Path', options=list(new_df.columns))
                    fig = px.sunburst(data_frame=new_df, path=path, values='New_Column', title= f'Sunburst Chart of All Selected Columns.')
                    st.plotly_chart(fig)
        
info = st.button("About Website")
if info == True:
    st.success('Thank You for Using Our Website...')
    st.success('More Details : ')
    st.success('Contact By : Jinal Kachhi - 9974132245 , Vatsal Shah - 8460963180')
