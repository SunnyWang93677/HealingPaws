package com.example.stage3_project2.Setting;

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.example.stage3_project2.Home.HomeFragment;
import com.example.stage3_project2.Login_Register.Login;
import com.example.stage3_project2.Pets.ViewPets;
import com.example.stage3_project2.R;

public class Emp_SettingFragment extends Fragment implements View.OnClickListener{

    Button viewPets;
    TextView logout;

    public Emp_SettingFragment() {

    }

    public static Emp_SettingFragment newInstance() {
        Emp_SettingFragment fragment = new Emp_SettingFragment();
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_emp_setting, container, false);
        init(view);
        return view;
    }

    private void init(View view){
//        viewPets = view.findViewById(R.id.viewPets);
//        viewPets.setOnClickListener(this);
        logout = view.findViewById(R.id.logOut);
        logout.setOnClickListener(this);
    }



    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.logOut:
                Intent intent = new Intent(getActivity(), Login.class);
                startActivity(intent);
                break;

        }
    }
}
