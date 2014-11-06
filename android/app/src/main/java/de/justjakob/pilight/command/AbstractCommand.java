package de.justjakob.pilight.command;

import android.util.Log;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

abstract public class AbstractCommand<T> {
    private String command;
    private String module;
    private JSONObject params;
    private int sequence = -1;
    private List<CommandResultReceiver<T>> receivers = new ArrayList<CommandResultReceiver<T>>();

    protected AbstractCommand(String command) {
        this.command = command;
    }

    public void setSequence(int sequence) {
        this.sequence = sequence;
    }

    public String toJson() {
        JSONObject o = new JSONObject();
        try {
            o.put("command", command);
            if (sequence >= 0) o.put("sequence", sequence);
            if (module != null) o.put("module", module);
            if (params != null) o.put("params", params);
        } catch (JSONException ignored) {
            return null;
        }
        return o.toString();
    }

    public void success(Object data) {
        Log.d("AbstractCommand", "got result: " + data.toString());
        T result = parseResult(data);
        for (CommandResultReceiver<T> receiver : receivers) receiver.receiveResult(result);
    }

    abstract protected T parseResult(Object data);

    public void failure() {
        Log.e("AbstractCommand", "command " + command + " failed");
    }

    public void addReceiver(CommandResultReceiver<T> receiver) {
        receivers.add(receiver);
    }

    public void setModule(String module) {
        this.module = module;
    }

    public void setParams(JSONObject params) {
        this.params = params;
    }
}
