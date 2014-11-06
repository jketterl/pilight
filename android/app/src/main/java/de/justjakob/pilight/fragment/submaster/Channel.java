package de.justjakob.pilight.fragment.submaster;

import android.util.Log;

import java.util.ArrayList;
import java.util.List;

import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.control.SubMaster;

public class Channel {
    private final SubMaster subMaster;

    public static interface OnValueChangedListener {
        public void valueChanged(int newValue);
    }

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
        if (newValue == value) return;
        target = newValue;
        if (held) return;
        held = true;
        subMaster.setChannelValue(this, newValue, new CommandResultReceiver<Object>() {
            @Override
            public void receiveResult(Object result) {
                held = false;
                if (target != value) setValue(target);
            }
        });
    }

    public void receiveValueUpdate(int newValue) {
        value = newValue;
        for (OnValueChangedListener l : listeners) l.valueChanged(newValue);
    }

    private List<OnValueChangedListener> listeners = new ArrayList<OnValueChangedListener>();

    public void addOnValueChangedListener(OnValueChangedListener listener) {
        listeners.add(listener);
    }

    public void removeOnValueChangedListener(OnValueChangedListener listener) {
        listeners.remove(listener);
    }
}
