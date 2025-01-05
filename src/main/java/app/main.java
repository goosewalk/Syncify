package app;

import data_access.DataAccessObject;
import org.json.JSONArray;
import org.json.JSONObject;

public class main {
    private static final String CLIENT_ID = "id";
    private static final String CLIENT_SECRET = "secret";
    private static final String USER_ID = "na4dbs6dsmemoj7yjpih3w16h";

    public static void main(String[] args) {
        try {
            String accessToken = DataAccessObject.getAccessToken(CLIENT_ID, CLIENT_SECRET);

            DataAccessObject spotifyDAO = new DataAccessObject(accessToken);

            JSONArray playlists = spotifyDAO.fetchPlaylists(USER_ID);

            // Print the playlists
            System.out.println("Your Playlists:");
            for (int i = 0; i < playlists.length(); i++) {
                JSONObject playlist = playlists.getJSONObject(i);
                String name = playlist.getString("name");
                System.out.println("- " + name);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
