package de.justjakob.pilight;

import android.app.Activity;
import android.appwidget.AppWidgetManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.DataSetObserver;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Spinner;
import android.widget.SpinnerAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.control.SubMaster;
import de.justjakob.pilight.fragment.submaster.Channel;


/**
 * The configuration screen for the {@link LightSwitchWidget LightSwitchWidget} AppWidget.
 */
public class LightSwitchWidgetConfigureActivity extends Activity {

    private static class SubmasterChannelAdapter implements SpinnerAdapter {

        private List<Channel> channels = Collections.emptyList();
        private Context context;
        private Handler h = new Handler(){
            @Override
            public void handleMessage(Message msg) {
                fireUpdated();
            }
        };

        public SubmasterChannelAdapter(Context context, SubMaster subMaster) {
            this.context = context;
            subMaster.getChannels(new CommandResultReceiver<List<Channel>>() {
                @Override
                public void receiveResult(List<Channel> result) {
                    channels = result;
                    h.sendEmptyMessage(0);
                }
            });
        }

        private void fireUpdated() {
            for (DataSetObserver o : observers) {
                o.onChanged();
            }
        }

        private List<DataSetObserver> observers = new ArrayList<>();

        @Override
        public View getDropDownView(int position, View convertView, ViewGroup parent) {
            return getView(position, convertView, parent);
        }

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
            return 0;
        }

        @Override
        public boolean hasStableIds() {
            return false;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            TextView text = new TextView(context);
            text.setTextColor(Color.BLACK);
            text.setText(((Channel) getItem(position)).getName());
            return text;
        }

        @Override
        public int getItemViewType(int position) {
            return 1;
        }

        @Override
        public int getViewTypeCount() {
            return 1;
        }

        @Override
        public boolean isEmpty() {
            return channels.size() > 0;
        }
    }

    int mAppWidgetId = AppWidgetManager.INVALID_APPWIDGET_ID;
    private static final String PREFS_NAME = "de.justjakob.pilight.LightSwitchWidget";
    private static final String PREF_PREFIX_KEY = "appwidget_";

    Spinner channelSelector;

    public LightSwitchWidgetConfigureActivity() {
        super();
    }

    @Override
    public void onCreate(Bundle icicle) {
        super.onCreate(icicle);

        // Set the result to CANCELED.  This will cause the widget host to cancel
        // out of the widget placement if the user presses the back button.
        setResult(RESULT_CANCELED);

        setContentView(R.layout.light_switch_widget_configure);
        findViewById(R.id.add_button).setOnClickListener(mOnClickListener);

        SubMaster subMaster = new SubMaster(this);
        // TODO this should not be hard-coded
        subMaster.setId("submaster");

        channelSelector = (Spinner) findViewById(R.id.channel_selector);
        channelSelector.setAdapter(new SubmasterChannelAdapter(this, subMaster));

        // Find the widget id from the intent.
        Intent intent = getIntent();
        Bundle extras = intent.getExtras();
        if (extras != null) {
            mAppWidgetId = extras.getInt(
                    AppWidgetManager.EXTRA_APPWIDGET_ID, AppWidgetManager.INVALID_APPWIDGET_ID);
        }

        // If this activity was started with an intent without an app widget ID, finish with an error.
        if (mAppWidgetId == AppWidgetManager.INVALID_APPWIDGET_ID) {
            finish();
            return;
        }

        //mAppWidgetText.setText(loadTitlePref(LightSwitchWidgetConfigureActivity.this, mAppWidgetId));
    }

    View.OnClickListener mOnClickListener = new View.OnClickListener() {
        public void onClick(View v) {
            final Context context = LightSwitchWidgetConfigureActivity.this;

            // When the button is clicked, store the string locally
            String channelName = ((Channel) channelSelector.getSelectedItem()).getName();
            saveTitlePref(context, mAppWidgetId, channelName);

            // It is the responsibility of the configuration activity to update the app widget
            AppWidgetManager appWidgetManager = AppWidgetManager.getInstance(context);
            LightSwitchWidget.updateAppWidget(context, appWidgetManager, mAppWidgetId);

            // Make sure we pass back the original appWidgetId
            Intent resultValue = new Intent();
            resultValue.putExtra(AppWidgetManager.EXTRA_APPWIDGET_ID, mAppWidgetId);
            setResult(RESULT_OK, resultValue);
            finish();
        }
    };

    // Write the prefix to the SharedPreferences object for this widget
    static void saveTitlePref(Context context, int appWidgetId, String text) {
        Log.d("LSWCA", "storing channel: " + text);
        SharedPreferences.Editor prefs = context.getSharedPreferences(PREFS_NAME, 0).edit();
        prefs.putString(PREF_PREFIX_KEY + appWidgetId, text);
        prefs.commit();
    }

    // Read the prefix from the SharedPreferences object for this widget.
    // If there is no preference saved, get the default from a resource
    static String loadTitlePref(Context context, int appWidgetId) {
        SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, 0);
        String titleValue = prefs.getString(PREF_PREFIX_KEY + appWidgetId, null);
        Log.d("LSCWA", "read channel: " + titleValue);
        return titleValue;
    }

    static void deleteTitlePref(Context context, int appWidgetId) {
        SharedPreferences.Editor prefs = context.getSharedPreferences(PREFS_NAME, 0).edit();
        prefs.remove(PREF_PREFIX_KEY + appWidgetId);
        prefs.commit();
    }
}



