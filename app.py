import streamlit as st
import pandas as pd
import plotly.express as px
# Load the dataFrame from data folder 
amazon_df = pd.read_csv("data/final_amazon_data.csv")
# Drop the Unnamed column from the dataFrame
amazon_df.drop(columns="Unnamed: 0", inplace=True)
# Set up the Streamlit app layout
st.title("Amazon Sales data Analysis")
st.write("Today i will make a Simple EDA Application for Amazon Sales datasets.")
data_set_url = "https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset"
st.write("Dataset link in Kaggle: [Amazon Sales dataset](%s)" % data_set_url)
st.sidebar.header("Navigation")
st.sidebar.markdown("Created by [Ahmed Yusri](www.linkedin.com/in/ahmed-yusri-499a67313)")
# Create an set of options for user to select
sidebar_option = st.sidebar.radio("Choose an Option:", ["Data Overview", "EDA", "Visualizations"])

# 1. Data Overview part 
if sidebar_option == "Data Overview":
    st.header("Data Overview")
    st.write("This dataset provides information about product name, user name, and product categories.")
    st.write(amazon_df.head())
    st.markdown("### Dataset Summary")
    st.write(amazon_df.describe())
    st.markdown("### Interactive Columns datatypes")
    selected_col = st.sidebar.selectbox("Select a column", amazon_df.columns)
    st.write(f"Datatype of {selected_col}: {amazon_df[selected_col].dtype}")
   
# 2. EDA part
elif sidebar_option == "EDA":
     st.header("Exploratory Data Analysis")
     
     # 1. Put a select radio to choose to see a uni or bivariant analysis
     analysis_type_option = st.sidebar.radio("Choose type of Analysis:", ["Univariant analysis", "Divariant analysis"])
     if analysis_type_option == "Univariant analysis":
         st.subheader("Univariant analysis")
         # 1.1 Plot a histogram of the rating column
         st.markdown("### Rating Distribution")
         fig1 = px.histogram(amazon_df, x='rating', nbins=20, title="Distribution of Rating")
         st.plotly_chart(fig1)
         # 1.2 Plot a histogram of the actual price column
         st.markdown("### Actual price Distribution")
         fig2 = px.histogram(amazon_df, x='actual_price', nbins=20, title="Distribution of Actual price")
         st.plotly_chart(fig2)
         
     elif analysis_type_option == "Divariant analysis":
         st.subheader("Divariant analysis")
         # 1.1 See the corrlation between actual_price and rating columns
         st.markdown("### Corrlation between actual price and rating columns")
         fig3 = px.scatter(x='rating',y='actual_price', data_frame=amazon_df); 
         st.plotly_chart(fig3) 
          
         # 1.2 See the corrlation between discount_price and actual_price columns
         fig4 = px.scatter(x='actual_price',
                           y='discounted_price', 
                           data_frame=amazon_df, 
                           title="Corrlation between actual price and discounted price columns"
                           )
         st.plotly_chart(fig4) 
         st.write("See the corrlation between actual price column and discount price is very high")
         # 1.3 Plot a heatmap plot
         st.markdown("### Heatmap plot")
         # See the headmap between all of the columns 
         corr_matrix = amazon_df.corr(numeric_only=True) # To get the numertic values 
         fig = px.imshow(
             corr_matrix,
             text_auto=True,             # Display correlation values on the heatmap
             color_continuous_scale="peach",
             zmin=-1, 
             zmax=1,
             labels=dict(x="Features", y="Features", color="Correlation")
             )
         st.plotly_chart(fig)
# 3. Visualizations part
elif sidebar_option == "Visualizations":
    st.header("Data Visualizations")
    
    # Pie chart for Number of most sold 10 product
    # 1. Create a new column called Product_type 
    amazon_df["product_type"] = amazon_df["category"].str.split("|").str.get(-1)
    # 2. Get the most 10 sold product types
    most_sold_10 = amazon_df["product_type"].value_counts().sort_values(ascending=False)[0:10]
    
    st.markdown("### Most 10 sold products")
    fig = px.pie(most_sold_10, 
             values=most_sold_10.values, 
             names=most_sold_10.index,
             title="Number of most sold 10 product"
            )
    fig.update_layout(width=500, height=500)
    st.plotly_chart(fig)
    # Create the bar plot using Plotly to see the most expensive products
    top_5_expensive = amazon_df.sort_values('discounted_price', ascending=False).head(5)    
    top_5_expensive['short_product_name'] = top_5_expensive['product_name'].apply(lambda x: x[:20] + '...' if len(x) > 20 else x)
    fig1 = px.bar(
        top_5_expensive,
        x='discounted_price',
        y='short_product_name',
        orientation='h',         # Horizontal bar chart for better readability
        title='Top 5 Most Expensive Products After Discount',
        labels={'discounted_price': 'Discounted Price', 'product_name': 'Product Name'},
        color='discounted_price', # Color based on discounted price for a gradient effect
        color_continuous_scale='Viridis'
    )

    # Update layout for better appearance
    fig1.update_layout(
    xaxis_title="Discounted Price",
    yaxis_title="Product Name",
    yaxis={'categoryorder':'total ascending'} # Orders bars from lowest to highest by discounted price
    )
    st.plotly_chart(fig1) 
    
    # Create the bar plot using Plotly to see the most cheapest  products
    top_5_cheapest = amazon_df.sort_values('discounted_price').head(5)

    # Shorten the product names for the y-axis (e.g., limit to 20 characters)
    top_5_cheapest['short_product_name'] = top_5_cheapest['product_name'].apply(lambda x: x[:20] + '...' if len(x) > 20 else x)

    # Create the bar plot using Plotly Express
    fig3 = px.bar(
        top_5_cheapest,
        x='discounted_price',
        y='short_product_name',  # Use the shortened product names
        orientation='h',         # Horizontal bar chart for better readability
        title='Top 5 Cheapest Products After Discount',
        labels={'discounted_price': 'Discounted Price', 'short_product_name': 'Product Name'},
        color='discounted_price', # Color based on discounted price for a gradient effect
        color_continuous_scale='Viridis'
    )
    fig3.update_layout(
    xaxis_title="Discounted Price",
    yaxis_title="Product Name",
    yaxis={'categoryorder':'total ascending'} # Orders bars from lowest to highest by discounted price
    )
    st.plotly_chart(fig3)


# Footer
st.sidebar.markdown("***")
st.sidebar.write("End of App")