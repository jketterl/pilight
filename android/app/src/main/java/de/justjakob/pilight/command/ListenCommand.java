package de.justjakob.pilight.command;

import de.justjakob.pilight.control.Controllable;

public class ListenCommand extends AbstractCommand<Object> {
    public ListenCommand(Controllable module) {
        super("listen");
        setModule(module);
    }

    @Override
    protected Object parseResult(Object data) {
        return null;
    }
}
