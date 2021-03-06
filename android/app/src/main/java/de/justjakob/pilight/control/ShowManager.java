package de.justjakob.pilight.control;

import android.app.Fragment;
import android.content.Context;
import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

import de.justjakob.pilight.command.AbstractCommand;
import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.connection.ConnectionService;
import de.justjakob.pilight.fragment.showmanager.Show;
import de.justjakob.pilight.fragment.showmanager.ShowManagerFragment;

public class ShowManager extends Controllable {
    private Context context;

    public ShowManager() {
        this.context = null;
    }

    public ShowManager(Context context) {
        this.context = context;
    }

    private class GetShowsCommand extends AbstractCommand<List<Show>> {
        protected GetShowsCommand() {
            super("getShows");
            setModule(ShowManager.this);
        }

        @Override
        protected List<Show> parseResult(Object data) {
            List<Show> result = new ArrayList<Show>();
            JSONArray arr = (JSONArray) data;
            for (int i = 0; i < arr.length(); i++) {
                Show s = new Show();
                try {
                    JSONObject o = arr.getJSONObject(i);
                    s.setId(o.getString("id"));
                    s.setName(o.getString("name"));
                    s.setRunning(o.getBoolean("running"));
                    result.add(s);
                } catch (JSONException e) {
                    Log.w("ShowManager", "could not parse response", e);
                }
            }
            return result;
        }
    }

    private class StopShowCommand extends AbstractCommand<Object> {

        protected StopShowCommand(Show show) {
            super("stopShow");
            setModule(ShowManager.this);
            JSONObject params = new JSONObject();
            try {
                params.put("id", show.getId());
            } catch (JSONException ignored) {}
            setParams(params);
        }

        @Override
        protected Object parseResult(Object data) {
            return null;
        }
    }

    private class StartShowComand extends AbstractCommand<Object> {
        protected StartShowComand(Show show) {
            super("startShow");
            setModule(ShowManager.this);
            JSONObject params = new JSONObject();
            try {
                params.put("id", show.getId());
            } catch (JSONException ignored) {}
            setParams(params);
        }

        @Override
        protected Object parseResult(Object data) {
            return null;
        }
    }

    @Override
    public String getDisplayName() {
        return "Show Manager";
    }

    @Override
    public Fragment getFragment() {
        return ShowManagerFragment.newInstance(getId());
    }

    @Override
    public void receiveMessage(JSONObject data) {
        try {
            String id = data.getString("show");
            Show s = findShow(id);
            if (s == null) return;
            s.setRunning(data.getBoolean("running"));
        } catch (JSONException e) {
            Log.w("ShowManager", "unexpected status update", e);
        }
    }

    private List<Show> shows;

    private Show findShow(String id) {
        if (shows == null) return null;
        for (Show s : shows) if (s.getId().equals(id)) return s;
        return null;
    }

    public void getShows(CommandResultReceiver<List<Show>> receiver) {
        GetShowsCommand c = new GetShowsCommand();
        c.addReceiver(receiver);
        c.addReceiver(new CommandResultReceiver<List<Show>>() {
            @Override
            public void receiveResult(List<Show> result) {
                shows = result;
            }
        });
        ConnectionService.runCommand(context, c);
    }

    public void stopShow(Show show) {
        StopShowCommand c = new StopShowCommand(show);
        ConnectionService.runCommand(context, c);
    }

    public void startShow(Show show) {
        StartShowComand c = new StartShowComand(show);
        ConnectionService.runCommand(context, c);
    }
}
