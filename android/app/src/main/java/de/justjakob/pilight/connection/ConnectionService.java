package de.justjakob.pilight.connection;

import android.app.Service;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Binder;
import android.os.IBinder;
import android.preference.PreferenceManager;
import android.util.Log;
import android.util.SparseArray;

import com.codebutler.android_websockets.WebSocketClient;

import org.json.JSONException;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;

import de.justjakob.pilight.command.AbstractCommand;

public class ConnectionService extends Service {
    private static final String TAG = "ConnectionService";

    public ConnectionService() {}

    private LocalBinder binder = new LocalBinder();

    private WebSocketClient client;

    public class LocalBinder extends Binder {
        public void runCommand(AbstractCommand command) {
            command.setSequence(++sequence);
            requests.put(sequence, command);
            WebSocketClient client = getClient();
            if (queue != null) {
                synchronized (queue) {
                    queue.add(command);
                }
            } else {
                client.send(command.toJson());
            }
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return binder;
    }

    private SharedPreferences prefs;
    private List<AbstractCommand> queue;
    private int sequence = 0;
    private SparseArray<AbstractCommand> requests = new SparseArray<AbstractCommand>();

    private SharedPreferences.OnSharedPreferenceChangeListener ospcl = new SharedPreferences.OnSharedPreferenceChangeListener() {
        @Override
        public void onSharedPreferenceChanged(SharedPreferences sharedPreferences, String key) {
            Log.d(TAG, "shared preferences for " + key + " changed");
            if (client == null) return;
            client.disconnect();
            client = null;
        }
    };

    private void registerPreferenceListener() {
        prefs = PreferenceManager.getDefaultSharedPreferences(this);
        prefs.registerOnSharedPreferenceChangeListener(ospcl);
    }

    @Override
    public void onCreate() {
        registerPreferenceListener();
        super.onCreate();
    }

    private WebSocketClient getClient() {
        if (client == null) {
            try {
                queue = new ArrayList<AbstractCommand>();

                String host = prefs.getString("server_host", "NONE");
                String port = prefs.getString("server_port", "8000");
                URI u = new URI("ws://" + host + ":" + port + "/control");
                Log.d(TAG, "connection uri: " + u.toString());
                client = new WebSocketClient(u, new WebSocketClient.Listener() {
                    @Override
                    public void onConnect() {
                        Log.d(TAG, "websocket connected; working off queue");
                        synchronized (queue) {
                            for (AbstractCommand command : queue) {
                                client.send(command.toJson());
                            }
                            queue = null;
                        }
                        Log.d(TAG, "websocket queue done");
                    }

                    @Override
                    public void onMessage(String message) {
                        parseResponse(message);
                    }

                    @Override
                    public void onMessage(byte[] data) {
                        Log.e(TAG, "received unsupported data message");
                    }

                    @Override
                    public void onDisconnect(int code, String reason) {
                        Log.d(TAG, "websocket disconnected");
                    }

                    @Override
                    public void onError(Exception error) {
                        Log.e(TAG, "websocket error", error);
                    }
                }, null);
                client.connect();
            } catch (URISyntaxException e) {
                Log.e(TAG, "uri error", e);
            }
        }
        return client;
    }

    private void parseResponse(String message) {
        Log.d(TAG, "parsing response: " + message);
        try {
            JSONObject response = new JSONObject(message);
            int sequence = response.getInt("sequence");
            AbstractCommand command = requests.get(sequence);
            if (command == null) {
                Log.w(TAG, "unable to find request #" + sequence);
            }
            if (response.get("status").equals("OK")) {
                command.success(response.get("data"));
            } else {
                command.failure();
            }
        } catch (JSONException e) {
            Log.w(TAG, "unable to parse JSON" , e);
        }
    }
}
