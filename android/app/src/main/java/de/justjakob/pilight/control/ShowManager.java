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
        protected GetShowsCommand(ShowManager m) {
            super("getShows");
            setModule(m);
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

    @Override
    public String getDisplayName() {
        return "Show Manager";
    }

    @Override
    public Fragment getFragment() {
        return ShowManagerFragment.newInstance(getId());
    }

    public void getShows(CommandResultReceiver<List<Show>> receiver) {
        GetShowsCommand c = new GetShowsCommand(this);
        c.addReceiver(receiver);
        ConnectionService.runCommand(context, c);
    }
}
