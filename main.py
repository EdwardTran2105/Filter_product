
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
import streamlit as st
import pandas as pd
# Function to fetch data from Lark Base API
def fetch_inventory_data():
    # Create client
    client = lark.Client.builder() \
        .app_id("cli_a6b08cd2e838502f") \
        .app_secret("zURasgrfm6VStaYzzNAYqlld8usD3Cn2") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # Construct request object
    request = ListAppTableRecordRequest.builder() \
        .app_token("SAnmbQyfMaOxOzsgxcMlBZ9WgQh") \
        .table_id("tblrUvzYYT8tbSPQ") \
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
            "tone màu": item.fields.get("Màu", ""),
            "Record ID": item.record_id,
            "Thực tồn": item.fields.get("Thực tồn (Tổng nhập - Tổng xuất)",""),
            "Tồn kho":item.fields.get("Tồn kho (Thực tồn - sale đặt)","")
        }
        records_container.append(record_data)
        sorted_data = sorted(records_container, key=lambda item: int(item['Thực tồn']))
    return sorted_data



# Function to filter data based on color and inventory quantity
def find_data(data, color, thucTon):
    # Tìm tất cả mã vật tư có màu tương ứng
    result = [item for item in data if item['tone màu'] == color and int(item['Thực tồn']) >= int(thucTon)]
    
    # Kiểm tra và in kết quả
    if result:
        df = pd.DataFrame(result, columns=['Mã vật tư', 'tone màu', 'Thực tồn', 'Tồn kho'])
        
        # Hiển thị bảng dữ liệu
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