package de.justjakob.pilight.fragment.submaster;

import android.net.Uri;
import android.os.Bundle;
import android.app.Fragment;
import android.os.Handler;
import android.os.Message;
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
 * Activities that contain this fragment must implement the
 * {@link SubMasterFragment.OnFragmentInteractionListener} interface
 * to handle interaction events.
 * Use the {@link SubMasterFragment#newInstance} factory method to
 * create an instance of this fragment.
 */
public class SubMasterFragment extends Fragment {
    private static final String ARG_CONTROLLABLE_ID = "controllableId";

    private SubMaster subMaster;

    private OnFragmentInteractionListener mListener;

    /**
     * Use this factory method to create a new instance of
     * this fragment using the provided parameters.
     *
     * @param controllableId ID of submaster
     * @return A new instance of fragment SubMasterFragment.
     */
    // TODO: Rename and change types and number of parameters
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

    // TODO: Rename method, update argument and hook method into UI event
    public void onButtonPressed(Uri uri) {
        if (mListener != null) {
            mListener.onFragmentInteraction(uri);
        }
    }

    /*
    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        try {
            mListener = (OnFragmentInteractionListener) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException(activity.toString()
                    + " must implement OnFragmentInteractionListener");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mListener = null;
    }
    */

    /**
     * This interface must be implemented by activities that contain this
     * fragment to allow an interaction in this fragment to be communicated
     * to the activity and potentially other fragments contained in that
     * activity.
     * <p/>
     * See the Android Training lesson <a href=
     * "http://developer.android.com/training/basics/fragments/communicating.html"
     * >Communicating with Other Fragments</a> for more information.
     */
    public interface OnFragmentInteractionListener {
        // TODO: Update argument type and name
        public void onFragmentInteraction(Uri uri);
    }

}
