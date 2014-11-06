package de.justjakob.pilight.fragment.showmanager;


import android.os.Bundle;
import android.app.Fragment;
import android.os.Handler;
import android.os.Message;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.Button;

import java.util.List;

import de.justjakob.pilight.R;
import de.justjakob.pilight.command.CommandResultReceiver;
import de.justjakob.pilight.control.ShowManager;

/**
 * A simple {@link Fragment} subclass.
 */
public class ShowManagerFragment extends Fragment {

    private static final String ARG_CONTROLLABLE_ID = "controllableId";

    private ShowManager showManager;

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param controllableId ID of submaster
     * @return A new instance of fragment SubMasterFragment.
     */
    public static ShowManagerFragment newInstance(String controllableId) {
        ShowManagerFragment fragment = new ShowManagerFragment();
        Bundle args = new Bundle();
        args.putString(ARG_CONTROLLABLE_ID, controllableId);
        fragment.setArguments(args);
        return fragment;
    }

    public ShowManagerFragment() {
        // Required empty public constructor
    }

    private Handler h = new Handler() {
        @Override
        public void handleMessage(Message msg) {
            List<Show> shows = (List<Show>) msg.obj;
            ShowListView slv = (ShowListView) getView().findViewById(R.id.showList);
            slv.setShows(shows);
        }
    };

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (getArguments() != null) {
            showManager = new ShowManager(getActivity());
            showManager.setId(getArguments().getString(ARG_CONTROLLABLE_ID));
        }

        showManager.getShows(new CommandResultReceiver<List<Show>>() {
            @Override
            public void receiveResult(List<Show> result) {
                Message msg = new Message();
                msg.obj = result;
                h.sendMessage(msg);
            }
        });
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View v =  inflater.inflate(R.layout.fragment_show_manager, container, false);

        Button stopAllButton = (Button) v.findViewById(R.id.stopAllButton);
        stopAllButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showManager.stopShow();
            }
        });

        final ShowListView slv = (ShowListView) v.findViewById(R.id.showList);
        slv.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                Show s = (Show) slv.getItemAtPosition(position);
                showManager.startShow(s);
            }
        });

        return v;
    }


}
