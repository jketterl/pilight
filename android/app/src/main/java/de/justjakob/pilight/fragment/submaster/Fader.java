package de.justjakob.pilight.fragment.submaster;

import android.content.Context;
import android.widget.LinearLayout;
import android.widget.SeekBar;
import android.widget.TextView;

public class Fader extends LinearLayout {
    private Channel channel;

    public static interface UpdateBlocker {
        public void blockUpdates();
        public void unblockUpdates();
    }

    private UpdateBlocker updateBlocker;

    public Fader(Context context, Channel channel, UpdateBlocker ub) {
        super(context);
        this.channel = channel;
        this.updateBlocker = ub;
        addViews();
    }

    private void addViews() {
        setOrientation(VERTICAL);

        TextView name = new TextView(getContext());
        name.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
        name.setText(channel.getName());
        addView(name);

        SeekBar fader = new SeekBar(getContext());
        fader.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));
        fader.setMax(255);
        fader.setProgress(channel.getValue());
        addView(fader);

        fader.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                channel.setValue(progress);
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                updateBlocker.blockUpdates();
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                updateBlocker.unblockUpdates();
            }
        });
    }
}
