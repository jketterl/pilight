package de.justjakob.pilight.control.submaster;

import android.util.Log;

import de.justjakob.pilight.control.SubMaster;

public class Channel {
    private final SubMaster subMaster;

    public String getName() {
        return name;
    }

    public int getValue() {
        return value;
    }

    private String name;
    private int value;

    public Channel(SubMaster subMaster, String name, int value) {
        this.subMaster = subMaster;
        this.name = name;
        this.value = value;
    }

    public void setValue(int value) {
        this.value = value;
        subMaster.setChannelValue(this, value);
    }
}
