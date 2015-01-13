package de.justjakob.pilight.fragment.controlserver;

import android.content.Context;
import android.database.DataSetObserver;
import android.os.Handler;
import android.os.Message;
import android.util.AttributeSet;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.List;

import de.justjakob.pilight.R;
import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.control.ControlServer;
import de.justjakob.pilight.control.Controllable;

public class ControllableListView extends ListView {
    private static final String TAG = "ControllableListView";

    private Context context;

    public ControllableListView(Context context) {
        super(context);
        this.context = context;
        loadItems();
    }

    public ControllableListView(Context context, AttributeSet attrs) {
        super(context, attrs);
        this.context = context;
        loadItems();
    }

    public ControllableListView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        this.context = context;
        loadItems();
    }

    private class ControllableListAdapter implements ListAdapter {
        private List<Controllable> controllables;

        public ControllableListAdapter(List<Controllable> controllables) {
            this.controllables = controllables;
        }

        @Override
        public boolean areAllItemsEnabled() {
            return true;
        }

        @Override
        public boolean isEnabled(int position) {
            return true;
        }

        @Override
        public void registerDataSetObserver(DataSetObserver observer) {

        }

        @Override
        public void unregisterDataSetObserver(DataSetObserver observer) {

        }

        @Override
        public int getCount() {
            return controllables.size();
        }

        @Override
        public Object getItem(int position) {
            return controllables.get(position);
        }

        @Override
        public long getItemId(int position) {
            return 0;
        }

        @Override
        public boolean hasStableIds() {
            return false;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            View v = convertView;
            if (v == null) {
                LayoutInflater inf = LayoutInflater.from(context);
                v = inf.inflate(R.layout.listitem_control_server, null);
            }

            Controllable c = controllables.get(position);
            TextView t = (TextView) v.findViewById(R.id.name);
            t.setText(c.getDisplayName());
            return v;
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

    private Handler h = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            setAdapter(new ControllableListAdapter((List<Controllable>) msg.obj));
        }
    };

    private void loadItems() {
        ControlServer cs = new ControlServer(getContext());
        Log.d(TAG, "getting controllables");
        cs.getControllables(new CommandResultReceiver<List<Controllable>>() {
            @Override
            public void receiveResult(List<Controllable> result) {
                Message m = new Message();
                m.obj = result;
                h.sendMessage(m);
            }
        });

    }
}