package de.justjakob.pilight.fragment.showmanager;

import android.content.Context;
import android.database.DataSetObserver;
import android.os.Handler;
import android.os.Message;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.CompoundButton;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.Switch;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

import de.justjakob.pilight.R;

public class ShowListView extends ListView {
    private Context context;

    public ShowListView(Context context) {
        super(context);
        this.context = context;
    }

    public ShowListView(Context context, AttributeSet attrs) {
        super(context, attrs);
        this.context = context;
    }

    public ShowListView(Context context, AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
        this.context = context;
    }

    public static interface ShowStartStopListener {
        public void startShow(Show show);
        public void stopShow(Show show);
    }

    private ShowStartStopListener listener;

    public void setShows(List<Show> shows) {
        setAdapter(new ShowListAdapter(shows));
    }

    public void setShowStartStopListener(ShowStartStopListener l) {
        listener = l;
    }

    private class ShowListAdapter implements ListAdapter {
        private List<Show> shows;

        private Handler refreshHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                for (DataSetObserver o : observers) o.onChanged();
            }
        };

        private Show.OnShowDataChangedListener osdcl = new Show.OnShowDataChangedListener() {
            @Override
            public void onShowDataChanged() {
                refreshHandler.sendEmptyMessage(0);
            }
        };

        public ShowListAdapter(List<Show> shows) {
            this.shows = shows;
            for (Show s : shows) s.addOnShowDataChangedListener(osdcl);
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
            return shows.size();
        }

        @Override
        public Object getItem(int position) {
            return shows.get(position);
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
            View v = convertView;
            if (v == null) {
                LayoutInflater inf = LayoutInflater.from(context);
                v = inf.inflate(R.layout.listitem_show_manager, null);
            }

            final Show s = shows.get(position);
            TextView t = (TextView) v.findViewById(R.id.name);
            t.setText(s.getName());

            Switch enabledSwitch = (Switch) v.findViewById(R.id.enabledSwitch);
            enabledSwitch.setChecked(s.isRunning());
            enabledSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
                @Override
                public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                    if (isChecked) {
                        listener.startShow(s);
                    } else {
                        listener.stopShow(s);
                    }
                }
            });

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
}
