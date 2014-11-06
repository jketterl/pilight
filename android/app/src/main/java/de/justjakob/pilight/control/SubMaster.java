package de.justjakob.pilight.control;

import android.app.Fragment;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.IBinder;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import de.justjakob.pilight.command.AbstractCommand;
import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.connection.ConnectionService;
import de.justjakob.pilight.fragment.submaster.Channel;
import de.justjakob.pilight.fragment.submaster.SubMasterFragment;

public class SubMaster extends Controllable {

    private final Context context;

    public SubMaster() {
        context = null;
    }

    public SubMaster(Context context) {
        this.context = context;
    }

    private class GetValuesCommand extends AbstractCommand<List<Channel>> {

        protected GetValuesCommand() {
            super("getValues");
            setModule(SubMaster.this.getId());
        }

        @Override
        protected List<Channel> parseResult(Object data) {
            List<Channel> result = new ArrayList<Channel>();
            JSONObject obj = (JSONObject) data;
            JSONArray names = obj.names();

            for (int i = 0; i < names.length(); i++) {
                try {
                    String name = names.getString(i);
                    result.add(new Channel(SubMaster.this, name, obj.getInt(name)));
                } catch (JSONException e) {
                    Log.w("SubMaster", "could not parse json", e);
                }
            }
            return result;
        }
    }

    private class SetChannelValueCommand extends AbstractCommand {
        protected SetChannelValueCommand(String channel, int value) {
            super("setChannelValue");
            setModule(SubMaster.this.getId());
            JSONObject params = new JSONObject();
            try {
                params.put("channel", channel);
                params.put("value", value);
            } catch (JSONException ignored) {}
            this.setParams(params);
        }

        @Override
        protected Object parseResult(Object data) {
            return null;
        }
    }

    @Override
    public String getDisplayName() {
        return "Submaster";
    }

    @Override
    public Fragment getFragment() {
        return SubMasterFragment.newInstance(getId());
    }

    public void getChannels(final CommandResultReceiver<List<Channel>> receiver) {
        GetValuesCommand c = new GetValuesCommand();
        c.addReceiver(receiver);
        ConnectionService.runCommand(context, c);
    }

    public void setChannelValue(Channel channel, int value, CommandResultReceiver<Object> receiver) {
        final SetChannelValueCommand c = new SetChannelValueCommand(channel.getName(), value);
        c.addReceiver(receiver);
        ConnectionService.runCommand(context, c);
    }
}
