package de.justjakob.pilight;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import java.util.List;

import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.control.SubMaster;
import de.justjakob.pilight.fragment.submaster.Channel;

public class LightSwitchService extends Service {
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        final String channelName = intent.getStringExtra("channel");
        final SubMaster subMaster = new SubMaster(this);
        // TODO this should not be here
        subMaster.setId("submaster");
        subMaster.getChannels(new CommandResultReceiver<List<Channel>>() {
            @Override
            public void receiveResult(List<Channel> result) {
                Channel c = null;
                for (Channel candidate : result) {
                    if (candidate.getName().equals(channelName)) c = candidate;
                }
                if (c == null) return;
                subMaster.setChannelValue(c, c.getValue() > 0 ? 0 : 255, new CommandResultReceiver<Object>() {
                    @Override
                    public void receiveResult(Object result) {
                        // NOOP
                    }
                });
            }
        });

        return START_NOT_STICKY;
    }
}
