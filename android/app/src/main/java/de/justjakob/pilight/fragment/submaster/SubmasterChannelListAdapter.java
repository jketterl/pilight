package de.justjakob.pilight.fragment.submaster;

import android.database.DataSetObserver;
import android.os.Handler;
import android.os.Message;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;

import java.util.ArrayList;
import java.util.List;

public class SubmasterChannelListAdapter implements ListAdapter {

    private final List<Channel> channels;

    Handler h = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            for (DataSetObserver o : observers) o.onChanged();
        }
    };

    public SubmasterChannelListAdapter(List<Channel> channels) {
        this.channels = channels;
        for (Channel c : channels) c.addOnValueChangedListener(new Channel.OnValueChangedListener() {
            @Override
            public void valueChanged(int newValue) {
                h.sendEmptyMessage(0);
            }
        });
    }

    @Override
    public boolean areAllItemsEnabled() {
        return true;
    }

    @Override
    public boolean isEnabled(int position) {
        return true;
    }

    private List<DataSetObserver> observers = new ArrayList<DataSetObserver>();

    @Override
    public void registerDataSetObserver(DataSetObserver observer) {
        observers.add(observer);
    }

    @Override
    public void unregisterDataSetObserver(DataSetObserver observer) {
        observers.remove(observer);
    }

    @Override
    public int getCount() {
        return channels.size();
    }

    @Override
    public Object getItem(int position) {
        return channels.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public boolean hasStableIds() {
        return false;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        return new Fader(parent.getContext(), channels.get(position));
    }

    @Override
    public int getItemViewType(int position) {
        return 0;
    }

    @Override
    public int getViewTypeCount() {
        return 1;
    }

    @Override
    public boolean isEmpty() {
        return false;
    }
}
