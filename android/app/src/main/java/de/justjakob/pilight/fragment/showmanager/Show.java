package de.justjakob.pilight.fragment.showmanager;

import java.util.ArrayList;
import java.util.List;

public class Show {
    public static interface OnShowDataChangedListener {
        public void onShowDataChanged();
    }

    private String id;
    private String name;
    private boolean running;
    private List<OnShowDataChangedListener> listeners = new ArrayList<OnShowDataChangedListener>();

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if (name.equals(this.name)) return;
        this.name = name;
        fireOnShowDataChanged();
    }

    public boolean isRunning() {
        return running;
    }

    public void setRunning(boolean running) {
        if (this.running == running) return;
        this.running = running;
        fireOnShowDataChanged();
    }

    public void addOnShowDataChangedListener(OnShowDataChangedListener l) {
        listeners.add(l);
    }
    public void removeOnShowDataChangedListener(OnShowDataChangedListener l) {
        listeners.remove(l);
    }

    private void fireOnShowDataChanged() {
        for (OnShowDataChangedListener l : listeners) l.onShowDataChanged();
    }
}
