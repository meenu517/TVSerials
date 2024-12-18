import streamlit as st
import json
import os
import pandas as pd

class LocalMemoryManager:
    def __init__(self, storage_file="local_memory.json"):
        self.storage_file = storage_file
        self._initialize_storage()

    def _initialize_storage(self):
        """Ensures the storage file exists and is properly initialized."""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, "w") as file:
                json.dump({}, file)

    def _load_data(self):
        """Loads data from the storage file."""
        with open(self.storage_file, "r") as file:
            return json.load(file)

    def _save_data(self, data):
        """Saves data to the storage file."""
        with open(self.storage_file, "w") as file:
            json.dump(data, file, indent=4)

    def set(self, key, value):
        """Stores a key-value pair in local memory."""
        data = self._load_data()
        data[key] = value
        self._save_data(data)

    def get(self, key):
        """Retrieves a value by key from local memory."""
        data = self._load_data()
        return data.get(key, None)

    def search_keys(self, search_term):
        """Searches for keys containing the given search term."""
        data = self._load_data()
        return {k: v for k, v in data.items() if search_term.lower() in k.lower()}

    def delete(self, key):
        """Deletes a key-value pair from local memory."""
        data = self._load_data()
        if key in data:
            del data[key]
            self._save_data(data)

    def clear(self):
        """Clears all data from local memory."""
        self._save_data({})

    def list_keys(self):
        """Lists all keys stored in local memory."""
        data = self._load_data()
        return list(data.keys())

    def get_all(self):
        """Returns all key-value pairs in local memory."""
        return self._load_data()

# Initialize Local Memory Manager
memory = LocalMemoryManager()

# Streamlit App
def main():
    st.set_page_config(page_title="Streamlit Local Memory Manager", page_icon="📺")
    st.title("Streamlit Local Memory Manager")

    # Tabs for navigation
    tab1, tab2, tab3 = st.tabs(["Store Data", "Retrieve Data", "Manage Memory"])

    with tab1:
        st.header("Store Data")
        key = st.text_input("Enter Key", placeholder="e.g., username")
        value = st.text_input("Enter Value", placeholder="e.g., johndoe")
        if st.button("Save Data"):
            if key and value:
                memory.set(key, value)
                st.success(f"Data saved: {key} = {value}")
            else:
                st.error("Both key and value are required!")

    with tab2:
        st.header("Retrieve Data")
        search_term = st.text_input("Enter Search Term for Key")
        if st.button("Search Keys"):
            results = memory.search_keys(search_term)
            if results:
                df = pd.DataFrame(list(results.items()), columns=["Key", "Value"])
                st.table(df)
            else:
                st.warning("No matching keys found!")

    with tab3:
        st.header("Manage Memory")

        if st.button("List All Data in Table"):
            all_data = memory.get_all()
            if all_data:
                df = pd.DataFrame(list(all_data.items()), columns=["Key", "Value"])
                st.table(df)
            else:
                st.warning("No data found!")

        edit_key = st.text_input("Enter Key to Edit")
        new_value = st.text_input("Enter New Value", key="edit_value")
        if st.button("Edit Key-Value"):
            if edit_key and new_value:
                if edit_key in memory.list_keys():
                    memory.set(edit_key, new_value)
                    st.success(f"Key '{edit_key}' updated with new value: {new_value}")
                else:
                    st.error("Key not found!")
            else:
                st.error("Both key and new value are required!")

        delete_key = st.text_input("Enter Key to Delete")
        if st.button("Delete Key"):
            memory.delete(delete_key)
            st.success(f"Key '{delete_key}' deleted successfully!")

        if st.button("Clear All Data"):
            memory.clear()
            st.success("All data cleared successfully!")

if __name__ == "__main__":
    main()
