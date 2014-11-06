package de.justjakob.pilight.control;

import android.app.Fragment;

public class ShowManager extends Controllable {
    @Override
    public String getDisplayName() {
        return "Show Manager";
    }

    @Override
    public Fragment getFragment() {
        return null;
    }
}
