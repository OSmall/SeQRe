package com.seqre.androidapp.ui.home;

import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.Observer;
import androidx.lifecycle.ViewModelProvider;

import com.seqre.androidapp.MainActivity;
import com.seqre.androidapp.QRScanning;
import com.seqre.androidapp.R;
import com.seqre.androidapp.databinding.FragmentHomeBinding;
import com.seqre.androidapp.ui.home.HomeViewModel;
import android.view.View;



public class HomeFragment extends Fragment implements View.OnClickListener {

    HomeViewModel homeViewModel;
    FragmentHomeBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {
        homeViewModel =
                new ViewModelProvider(this).get(HomeViewModel.class);

        binding = FragmentHomeBinding.inflate(inflater, container, false);
        View root = binding.getRoot();

        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

    @Override
    public void onClick(View v) {
        TextView txt = findViewById(R.id.txtResultsHeader);
        txt.setText("Working");

        switch (v.getId()) {
            case R.id.camera_capture_button:
                startActivity(new Intent(HomeViewModel, QRScanning.class));
                break;
        }
    }
}