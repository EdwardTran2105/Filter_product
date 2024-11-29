
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
from lark_oapi.api.task.v2 import *
import streamlit as st
import pandas as pd
# Function to fetch data from Lark Base API
def fetch_inventory_data():
    try:
        # Create client
        client = lark.Client.builder() \
            .app_id("cli_a6b08cd2e838502f") \
            .app_secret("zURasgrfm6VStaYzzNAYqlld8usD3Cn2") \
            .log_level(lark.LogLevel.DEBUG) \
            .build()

        # Initialize request
        request = ListAppTableRecordRequest.builder() \
                .app_token("SAnmbQyfMaOxOzsgxcMlBZ9WgQh") \
                .table_id("tblrUvzYYT8tbSPQ") \
                .build()

        records_container = []

        # Fetch the first page
        response = client.bitable.v1.app_table_record.list(request)

        # Check if response is successful and contains data
        if not response.success():
            st.error(f"Failed to fetch data: {response.code}, {response.msg}")
            return None

        if not response.data or not hasattr(response.data, 'items'):
            st.error("No data found in the API response.")
            return None

        # Process first page
        for item in response.data.items:
            record_data = {
                "Mã vật tư": item.fields.get("Mã vật tư", ""),
                "tone màu": item.fields.get("tone màu", ""),
                "Thực tồn": item.fields.get("Thực tồn (m2)", ""),
                "Tồn kho": item.fields.get("Tồn kho (m2)", ""),
            }
            records_container.append(record_data)

        # Fetch subsequent pages
        while response.data.has_more:
            page_token = response.data.page_token
            request = ListAppTableRecordRequest.builder() \
                .app_token("SAnmbQyfMaOxOzsgxcMlBZ9WgQh") \
                .table_id("tblrUvzYYT8tbSPQ") \
                .page_token(page_token) \
                .build()

            response = client.bitable.v1.app_table_record.list(request)

            # Check response validity for each page
            if not response.success():
                st.error(f"Failed to fetch data on subsequent pages: {response.code}, {response.msg}")
                return None

            if not response.data or not hasattr(response.data, 'items'):
                st.warning("No more items found.")
                break

            # Process items on the current page
            for item in response.data.items:  
                record_data = {
                    "Mã vật tư": item.fields.get("Mã vật tư", ""),
                    "tone màu": item.fields.get("tone màu", ""),
                    "Thực tồn": item.fields.get("Thực tồn (m2)", ""),
                    "Tồn kho": item.fields.get("Tồn kho (m2)", ""),
                }
                records_container.append(record_data)

        # Sort data
        sorted_data = sorted(records_container, key=lambda item: float(item['Thực tồn']) if item['Thực tồn'] else 0)
        return sorted_data

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None




# Function to filter data based on color and inventory quantity
def find_data(data, color, thucTon):
    # Tìm tất cả mã vật tư có màu tương ứng
    result = [item for item in data if float(item['Thực tồn']) >= float(thucTon) and color == item['tone màu']]
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

    
    # Inputs
    colors = ["gỗ hương", "gỗ sồi", "gỗ óc chó", "lông sói", "gỗ sồi trắng", "khác"]

# Sử dụng selectbox để tạo dropdown
    color = st.selectbox("Select Color:", colors)
# Hiển thị kết quả được chọn
    tonkho = st.number_input("Enter Minimum Inventory Quantity:", min_value=0)
    data = fetch_inventory_data()
    if st.button("Query"):
        # Fetch data
        
        if data is None:
            st.stop()
        if color:
            
            filtered_data = find_data(data, color, tonkho)
            st.write(filtered_data)
        else:
            st.write("Please enter a color to query.")

if __name__ == "__main__":
    main()