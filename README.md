![mockup_ln6slhru](https://github.com/smellycloud/chart_to_playlist_api/assets/52908667/49424162-fcfc-4e38-85f2-341defe9c92a)
**Disclaimer:** Please ensure compliance with Spotify's terms of service and API usage policies when using this tool.

# Guide

### Follow these steps to set up and run the project on your local machine:
(I'm too cheap to deploy and host :3)

1. **Clone the Repository**
2. **Install Requirements**
   Navigate to the project directory and install the required packages by running:
   `pip install -r requirements.txt`
3. **Spotify Developer Credentials**
   * Go to Spotify Developer Dashboard and log in or create an account.
   * Create a Spotify Developer App and note down the Client ID and Client Secret.
   * Set the Redirect URI for your app to http://localhost:8080.
   * In the User Management section, add your name and the email of your Spotify account.
4. **Environment Variables**
   Create a `.env` file in the project directory and enter your Spotify Developer App credentials:
   `CLIENT_ID=your_client_id_here`,
   `CLIENT_SECRET=your_client_secret_here`
5. **Run the Server**
   Start the server using uvicorn. Run the following command from the project directory:
   `uvicorn main:app --reload`
6. **Generate Playlists**
   * Open your web browser and check the page_urls section in main.py to identify compatible charts. For example, to create a playlist called "Netherlands Songs 2023-01-21," visit: `http://127.0.0.1:8000/billboard_world/netherlands_songs/2023-01-21`.
   * To create a playlist called "Billboard 200 Global 2023-01-21" with the global top 200 songs, visit: `http://127.0.0.1:8000/billboard200_global/2023-01-21`
<img width="1007" alt="SCR-20231001-dadv" src="https://github.com/smellycloud/chart_to_playlist_api/assets/52908667/c2940ab9-d89f-458d-9609-2d67d55603bd">

7. **Profit**

**Note:** Some useful playlist information from Spotify is stored as Pandas DataFrames, which can be found in the `/data` directory. These DataFrames can be used for further analysis if necessary.
<img width="1833" alt="SCR-20231001-djax" src="https://github.com/smellycloud/chart_to_playlist_api/assets/52908667/d95fd2fe-d95a-4ae2-85f7-2bcd8a08d94e">

### Todo:
1. Write custom exceptions
2. Unify Billboard and BillboardWorld
3. Maybe build a companion mobile/desktop application
4. Integrate genre charts
5. Build a recommender system? Hmm.

