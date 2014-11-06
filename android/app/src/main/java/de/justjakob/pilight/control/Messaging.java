package de.justjakob.pilight.control;

import android.app.Fragment;

import org.json.JSONObject;

public class Messaging extends Controllable {
    @Override
    public String getDisplayName() {
        return "Messages";
    }

    @Override
    public Fragment getFragment() {
        return null;
    }

    @Override
    public void receiveMessage(JSONObject data) {

    }
}
