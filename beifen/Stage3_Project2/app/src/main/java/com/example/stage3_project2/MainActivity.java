package com.example.stage3_project2;

import android.support.v4.app.Fragment;
import android.support.annotation.IdRes;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.RadioGroup;

import com.example.stage3_project2.Appointment.AppointmentFragment;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private RadioGroup mRgTab;
    private List<Fragment> mFragmentList = new ArrayList<>();


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mRgTab = (RadioGroup) findViewById(R.id.rg_main);
        mRgTab.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, @IdRes int checkedId) {
                switch (checkedId) {
                    case R.id.rb_home:
                        changeFragment(HomeFragment.class.getName());
                        break;
                    case R.id.rb_appointment:
                        changeFragment(AppointmentFragment.class.getName());
                        break;
//                    case R.id.rb_find:
//                        changeFragment(FindFragment.class.getName());
//                        break;
//                    case R.id.rb_me:
//                        changeFragment(MeFragment.class.getName());
//                        break;
                }
            }
        });
        if(savedInstanceState == null){
            changeFragment(HomeFragment.class.getName());
        }
        init();
    }

    private void init(){


    }

    /**
     * show target fragment
     *
     * @param tag
     */
    public void changeFragment(String tag) {

        hideFragment();
        FragmentManager fm = getSupportFragmentManager();
        android.support.v4.app.FragmentTransaction ft = fm.beginTransaction();
        Fragment fragment = fm.findFragmentByTag(tag);

        if (fragment != null) {
            ft.show(fragment);
        } else {
            if (tag.equals(HomeFragment.class.getName())) {
                fragment = HomeFragment.newInstance();
            } else if (tag.equals(AppointmentFragment.class.getName())) {
                fragment = AppointmentFragment.newInstance();
            } //else if (tag.equals(ChatFragment.class.getName())) {
//                fragment = ChatFragment.newInstance();
//            } else if (tag.equals(SetFragement.class.getName())) {
//                fragment = SetFragement.newInstance();
//            }
            mFragmentList.add(fragment);
            ft.add(R.id.fl_container, fragment, fragment.getClass().getName());
        }
        ft.commitAllowingStateLoss();

    }

    /**
     * hide all fragment
     */
    private void hideFragment() {
        FragmentManager fm = getSupportFragmentManager();
        FragmentTransaction ft = fm.beginTransaction();
        for (Fragment f : mFragmentList) {
            ft.hide(f);
        }
        ft.commit();
    }



}
