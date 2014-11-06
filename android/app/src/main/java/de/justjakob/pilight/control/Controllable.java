package de.justjakob.pilight.control;

import android.app.Activity;
import android.app.Fragment;

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


}
