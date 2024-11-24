
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
import streamlit as st
import pandas as pd
# Function to fetch data from Lark Base API
def fetch_inventory_data():
    # Create client
    client = lark.Client.builder() \
        .app_id("cli_a63f1c47b3b8d010") \
        .app_secret("hRcpoJJ3WDr0K0w9kR0T6eVJ7y0pDhEX") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # Construct request object
    request = ListAppTableRecordRequest.builder() \
        .app_token("IkF8bLyBBau9desAkQllY8JKgud") \
        .table_id("tbloP02DaJyGPE2Q") \
        .build()

    # Make the request
    response = client.bitable.v1.app_table_record.list(request)

    # Handle failed response
    if not response.success():
        st.error(f"Failed to fetch data: {response.code}, {response.msg}")
        return None
    
    records_container = []
    # Process the data
    for item in response.data.items:
        record_data = {
            "Mã vật tư": item.fields.get("Mã vật tư", ""),
            "Màu": item.fields.get("Màu", ""),
            "Record ID": item.record_id,
            "m2": item.fields.get("m2","")
        }
        records_container.append(record_data)
        sorted_data = sorted(records_container, key=lambda item: int(item['m2']))
    return sorted_data

# Function to filter data based on color and inventory quantity
def find_data(data, color,m2):
    # Tìm tất cả mã vật tư có màu tương ứng
    result = [item for item in data if item['Màu'] == color and int(item['m2']) >= int(m2)]
    
    
    # Kiểm tra và in kết quả
    if result:
        df = pd.DataFrame(result, columns=['Mã vật tư', 'Màu', 'm2'])
        
        # Hiển thị bảng dữ liệu
        st.write(f"Các mã vật tư có màu {color} và m2 >= {m2} là:")
        st.write(df)
    else:
        st.write(f"Không tìm thấy mã vật tư nào có màu {color}.")

# Streamlit app
def main():
    st.title("Inventory Query App")

    # Fetch data
    data = fetch_inventory_data()
    if data is None:
        st.stop()

    # Inputs
    color = st.text_input("Enter Color:")
    tonkho = st.number_input("Enter Minimum Inventory Quantity:", min_value=0)

    if st.button("Query"):
        if color:
            filtered_data = find_data(data, color, tonkho)
            st.write(filtered_data)
        else:
            st.write("Please enter a color to query.")

if __name__ == "__main__":
    main()