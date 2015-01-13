package de.justjakob.pilight.command;

public interface CommandResultReceiver<T> {
    public void receiveResult(T result);
}
