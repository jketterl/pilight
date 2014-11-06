package de.justjakob.pilight.fragment.submaster;

import android.util.Log;

import de.justjakob.pilight.command.CommandResultReceiver;
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
    private int target;
    private boolean held = false;

    public Channel(SubMaster subMaster, String name, int value) {
        this.subMaster = subMaster;
        this.name = name;
        this.value = value;
        this.target = value;
    }

    public void setValue(final int newValue) {
        this.target = newValue;
        if (held) return;
        held = true;
        subMaster.setChannelValue(this, newValue, new CommandResultReceiver<Object>() {
            @Override
            public void receiveResult(Object result) {
                held = false;
                value = newValue;
                if (target != value) setValue(target);
            }
        });
    }
}
