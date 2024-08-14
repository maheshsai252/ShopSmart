import streamlit as st
import ast
import requests

def image_interface_cart(image_urls):
    image_urls = ast.literal_eval(image_urls)
    horizontal_scroll_html = """
        <div style="overflow-x: auto; white-space: nowrap;">
            %s
        </div>
    """

    # Generate HTML for displaying images
    images_html = " ".join(f'<img src="{url}" style="width:200px; margin-right:10px;" />' for url in image_urls)

    # Combine HTML templates and display
    st.write(horizontal_scroll_html % images_html, unsafe_allow_html=True)

# Function to generate consistent-sized images in a horizontal scroll
def image_interface(image_urls):
    try:
        image_urls = ast.literal_eval(image_urls)
        images_html = ""
        for url in image_urls:
            response = requests.head(url)
            if response.status_code == 200:
                images_html += f'<img src="{url}" style="width:150px; height:150px; object-fit: cover; margin-right: 10px;" />'
        return f"<div style='overflow-x: auto; white-space: nowrap;'>{images_html}</div>"
    except:
        return ""