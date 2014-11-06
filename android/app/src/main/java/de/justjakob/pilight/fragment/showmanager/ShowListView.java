package de.justjakob.pilight.fragment.showmanager;

import android.content.Context;
import android.database.DataSetObserver;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;

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

    public void setShows(List<Show> shows) {
        setAdapter(new ShowListAdapter(shows));
    }

    private class ShowListAdapter implements ListAdapter {
        private List<Show> shows;

        public ShowListAdapter(List<Show> shows) {
            this.shows = shows;
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

            Show s = shows.get(position);
            TextView t = (TextView) v.findViewById(R.id.name);
            t.setText(s.getName());
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
