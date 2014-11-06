package de.justjakob.pilight.fragment.submaster;

import android.os.Bundle;
import android.app.Fragment;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import java.util.List;

import de.justjakob.pilight.R;
import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.control.SubMaster;

/**
 * A simple {@link Fragment} subclass.
 * Use the {@link SubMasterFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class SubMasterFragment extends Fragment {
    private static final String ARG_CONTROLLABLE_ID = "controllableId";

    private SubMaster subMaster;

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param controllableId ID of submaster
     * @return A new instance of fragment SubMasterFragment.
     */
    public static SubMasterFragment newInstance(String controllableId) {
        SubMasterFragment fragment = new SubMasterFragment();
        Bundle args = new Bundle();
        args.putString(ARG_CONTROLLABLE_ID, controllableId);
        fragment.setArguments(args);
        return fragment;
    }

    public SubMasterFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            subMaster = new SubMaster(getActivity());
            subMaster.setId(getArguments().getString(ARG_CONTROLLABLE_ID));
        }

        subMaster.getChannels(new CommandResultReceiver<List<Channel>>() {
            @Override
            public void receiveResult(List<Channel> result) {
                Message msg = new Message();
                msg.obj = result;
                h.sendMessage(msg);
            }
        });
    }

    private Handler h = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            ListView faderList = (ListView) getView().findViewById(R.id.faderList);
            faderList.setAdapter(new SubmasterChannelListAdapter((List<Channel>) msg.obj));
        }
    };

    @Override
    public View onCreateView(LayoutInflater inflater, final ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_sub_master, container, false);
    }

}
