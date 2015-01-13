package de.justjakob.pilight.control;

import android.app.Fragment;
import android.content.Context;

import org.json.JSONObject;

import de.justjakob.pilight.connection.ConnectionService;

abstract public class Controllable {
    private String id;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    abstract public String getDisplayName();

    abstract public Fragment getFragment();

    public void listen(Context context) {
        ConnectionService.listen(context, this);
    }

    public void stopListening(Context context) {
        ConnectionService.stopListening(context, this);
    }

    public abstract void receiveMessage(JSONObject data);
}
