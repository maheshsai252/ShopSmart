import requests
import streamlit as st
from search.message.images import image_interface


# Function to get user activities from Snowflake
def get_user_activities():
    url = "http://chat-be-service:8000/get-activities/"
    json_req = {
        "userid": st.session_state.get('user_id', 1),
      }
    response = requests.get(url, params=json_req)
    try:
        return response.json()["response"] if "response" in response.json() else []
    except:
        return []

# Function to get product suggestions
def get_suggestions():
    url = "http://chat-be-service:8000/user-recommendations/"
    
    json_req = {
        "user_id": st.session_state.get('user_id', 1),
    }
    response = requests.get(url, params=json_req)
    try:
        if response.status_code == 200:
            return response.json()["response"] if "response" in response.json() else None
        else:
            st.error(f"Request failed with status code: {response}")
            return {}
    except:
        return {}

# Function to display suggested products in card format
def suggested_products():
    response = get_suggestions()
    
    if response is None:
        return
    
    # Retrieve user activities
    user_activities = get_user_activities()

    if user_activities:
        # Display user activities in a rectangular box with a pink shade
        box_style = (
            "border: 1px solid #ddd; padding: 10px; border-radius: 10px; background-color: #f9f9f9; text-align: center;"
        )
        badge_style = "display: inline-block; padding: 6px 12px; background-color: #ff9aa2; border-radius: 15px; margin: 5px; color: #333; font-size: 14px;"

        badges_html = " ".join([
            f"<span style='{badge_style}'>{activity}</span>"
            for activity in user_activities
        ])

        st.markdown(
            f"<div style='{box_style}'>"
            f"<h3 style='color: #e57373; font-size: 18px;'>Your Favorite Pastimes Activities 🏋️ 💃🏻 🧗🏻</h3>"
            f"{badges_html}"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Add a title for product recommendations
    st.markdown("<h2 style='color: #333;'>Products You May Like... 🏷️ 👜</h2>", unsafe_allow_html=True)
    st.markdown(
            f"<p style='color: #black; font-size: 18px;'>These products are recommended based on you chat search and your favourite activities ...</h3>",
            unsafe_allow_html=True,
        )
    # Add a one-line gap between the category title and product display
    st.markdown(" ")  # Creates the desired space

    refresh = st.button("Refresh Recommendations")
    if refresh:
        response = get_suggestions()
    # Iterate through product categories
    for cat in response.keys():
        # Add a bubble background with lavender shade, centered, and smaller
        st.markdown(
            f"<div style='background-color: #e6e6fa; border-radius: 10px; padding: 5px; width: 100%; text-align: center;'>"
            f"<h3 style='color: #7a5880; font-size: 18px;'>{cat}</h3>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Add another one-line gap after the category title
        st.markdown(" ")  # Consistent spacing

        # Group products into two columns for each row
        product_pairs = [response[cat][i:i + 2] for i in range(0, len(response[cat]), 2)]

        for product_pair in product_pairs:
            cols = st.columns(2)

            # Display each product in its respective column
            for idx, product in enumerate(product_pair):
                card_style = (
                    f"border: 1px solid #ddd; padding: 15px; border-radius: 10px; "
                    f"background-color: #f9f9f9; min-height: 300px; min-width: 250px; "
                    f"text-align: center;"
                )

                image_html = image_interface(product['imageURLHighRes'])

                card_content = (
                    f"<div class='product-card' style='{card_style}'>"
                    f"  {image_html}"
                    f"  <div style='margin-top: 10px;'>"
                    f"    <h3 style='color: #333; font-weight: bold;'>{product['title']}</h3>"
                    f"    <p style='color: #555; font-size: 14px; line-height: 1.5;'>{product['summary']}</p>"
                    f"    <p style='color: #888; font-size: 12px; font-style: italic;'>ASIN: {product['asin']}</p>"
                    f"  </div>"
                    f"</div>"
                )

                cols[idx].markdown(card_content, unsafe_allow_html=True)

            st.write("---")
