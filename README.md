# YouTube_Data_Harvesting_MongoDB_Streamlit

This Streamlit app allows users to fetch and visualize data from YouTube channels and videos. It utilizes the YouTube Data API to retrieve information such as channel statistics, video details, and comments. Users can also upload the fetched data to a MongoDB database.

## Features

- **YouTube Channel Viewer**: Enter a YouTube channel ID to view channel statistics, including subscribers, total views, and total videos. You can also upload this data to a MongoDB database.

- **YouTube Video Viewer**: Enter a YouTube video URL to view video details such as likes, duration, and comments. Similar to the channel viewer, you can upload this data to a MongoDB database.

## Screenshots

![Screenshot 2024-04-10 033821](https://github.com/Greatmonkeysden/YouTube_Data_Harvesting_MongoDB_Streamlit/assets/142253069/617c2ea3-4a3c-407c-9df0-b02412b6daab)

![Screenshot 2024-04-10 035725](https://github.com/Greatmonkeysden/YouTube_Data_Harvesting_MongoDB_Streamlit/assets/142253069/2a0b1f27-2a30-4638-a8c7-94158f40c476)

## Requirements

- Python 3
- Streamlit
- Google API Client Library
- pymongo
- Streamlit Option Menu (custom component for the sidebar option menu)

## Usage

Enter your YouTube API Key in the sidebar.

Choose between the "YouTube Channel" or "YouTube Video" options from the sidebar.

## Depending on your selection:

For YouTube Channel: Enter the channel ID and click "Get Channel Data" to view channel statistics. Click "Upload to MongoDB" to save the data to a MongoDB database.
For YouTube Video: Enter the video URL and click "Get Data" to view video details and comments. Click "Upload to database" to save the data to a MongoDB database.

## Contributing
Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

Feel free to adjust the content as needed for your specific project.


