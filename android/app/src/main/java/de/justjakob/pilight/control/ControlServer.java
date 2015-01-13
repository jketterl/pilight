package de.justjakob.pilight.control;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.IBinder;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import de.justjakob.pilight.command.AbstractCommand;
import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.connection.ConnectionService;

public class ControlServer {
    private static final String TAG = "ControlServer";

    private final Context context;

    public ControlServer() {
        this.context = null;
    }

    public ControlServer(Context context) {
        this.context = context;
    }

    private static class GetControllablesCommand extends AbstractCommand<List<Controllable>> {
        protected GetControllablesCommand() {
            super("getControllables");
        }

        @Override
        protected List<Controllable> parseResult(Object data) {
            JSONArray arr = (JSONArray) data;
            List<Controllable> result = new ArrayList<Controllable>();
            for (int i = 0; i < arr.length(); i++) {
                String type = "<unknown>";
                try {
                    JSONObject o = arr.getJSONObject(i);
                    type = o.getString("type");
                    String id = o.getString("id");
                    Class cls = Class.forName("de.justjakob.pilight.control." + type);
                    if (!Controllable.class.isAssignableFrom(cls)) {
                        Log.w(TAG, "is not a controllable: " + type);
                    } else {
                        Controllable c = (Controllable) cls.newInstance();
                        c.setId(id);
                        result.add(c);
                    }
                } catch (JSONException e) {
                    Log.w(TAG, "JSON error", e);
                } catch (ClassNotFoundException e) {
                    Log.w(TAG, "could not instantiate controllable; no class for name \"" + type + "\"");
                } catch (InstantiationException e) {
                    Log.e(TAG, "could not instantiate controllable", e);
                } catch (IllegalAccessException e) {
                    Log.e(TAG, "could not instantiate controllable", e);
                }
            }
            return result;
        }
    }

    public void getControllables(final CommandResultReceiver<List<Controllable>> receiver) {
        GetControllablesCommand command = new GetControllablesCommand();
        command.addReceiver(receiver);
        ConnectionService.runCommand(context, command);
    }
}
