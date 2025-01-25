package de.justjakob.pilight;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.widget.RemoteViews;

public class LightSwitchWidget extends AppWidgetProvider {

    public static final String LIGHTSWITCH_ACTION = "LightSwitchAction";

    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals(LIGHTSWITCH_ACTION)) {
            int appWidgetId = intent.getIntExtra("widgetId", -1);
            CharSequence channelName = intent.getCharSequenceExtra("channel");

            Intent i = new Intent(context, LightSwitchService.class);
            i.putExtra("channel", channelName);
            context.startService(i);
            return;
        }
        super.onReceive(context, intent);
    }

    @Override
    public void onUpdate(Context context, AppWidgetManager appWidgetManager, int[] appWidgetIds) {
        // There may be multiple widgets active, so update all of them
        final int N = appWidgetIds.length;
        for (int i = 0; i < N; i++) {
            updateAppWidget(context, appWidgetManager, appWidgetIds[i]);
        }
    }

    @Override
    public void onDeleted(Context context, int[] appWidgetIds) {
        // When the user deletes the widget, delete the preference associated with it.
        final int N = appWidgetIds.length;
        for (int i = 0; i < N; i++) {
            LightSwitchWidgetConfigureActivity.deleteTitlePref(context, appWidgetIds[i]);
        }
    }

    @Override
    public void onEnabled(Context context) {
        // Enter relevant functionality for when the first widget is created
    }

    @Override
    public void onDisabled(Context context) {
        // Enter relevant functionality for when the last widget is disabled
    }

    static void updateAppWidget(Context context, AppWidgetManager appWidgetManager,
                                int appWidgetId) {

        CharSequence channelName = LightSwitchWidgetConfigureActivity.loadTitlePref(context, appWidgetId);
        // Construct the RemoteViews object
        RemoteViews views = new RemoteViews(context.getPackageName(), R.layout.light_switch_widget);
        if (channelName != null) views.setCharSequence(R.id.lightswitch, "setText", channelName);

        Intent intent = new Intent(context, LightSwitchWidget.class);
        // Data is necessary to make the Intents unique
        intent.setData(Uri.parse("pilight://submaster/" + channelName));
        intent.setAction(LIGHTSWITCH_ACTION);
        intent.putExtra("widgetId", appWidgetId);
        intent.putExtra("channel", channelName);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(context, 0, intent, Intent.FILL_IN_DATA | PendingIntent.FLAG_IMMUTABLE);
        views.setOnClickPendingIntent(R.id.lightswitch, pendingIntent);

        // Instruct the widget manager to update the widget
        appWidgetManager.updateAppWidget(appWidgetId, views);
    }
}


