package data_access;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import org.json.JSONArray;
import org.json.JSONObject;

public class DataAccessObject {
    private static final String TOKEN_URL = "https://accounts.spotify.com/api/token";
    private static final String PLAYLISTS_URL = "https://api.spotify.com/v1/users/{user_id}/playlists";
    private final String accessToken;

    public DataAccessObject(String accessToken) {
        this.accessToken = accessToken;
    }

    // Fetch playlists
    public JSONArray fetchPlaylists(String userId) throws Exception {
        String url = PLAYLISTS_URL.replace("{user_id}", userId);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Authorization", "Bearer " + accessToken)
                .build();

        HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        JSONObject jsonResponse = new JSONObject(response.body());
        System.out.println(jsonResponse);
        return jsonResponse.getJSONArray("items");
    }

    // Retrieve access token
    public static String getAccessToken(String clientId, String clientSecret) throws Exception {
        String auth = clientId + ":" + clientSecret;
        String encodedAuth = java.util.Base64.getEncoder().encodeToString(auth.getBytes());

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(TOKEN_URL))
                .header("Authorization", "Basic " + encodedAuth)
                .header("Content-Type", "application/x-www-form-urlencoded")
                .POST(HttpRequest.BodyPublishers.ofString("grant_type=client_credentials"))
                .build();

        HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        JSONObject jsonResponse = new JSONObject(response.body());
        return jsonResponse.getString("access_token");
    }
}
