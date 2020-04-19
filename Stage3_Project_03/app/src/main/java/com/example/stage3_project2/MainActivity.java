package com.example.stage3_project2;

import android.content.Intent;
import android.support.v4.app.Fragment;
import android.support.annotation.IdRes;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.RadioGroup;

import com.example.stage3_project2.Appointment.AppointmentFragment;
import com.example.stage3_project2.Home.HomeFragment;
import com.example.stage3_project2.Question.QuestionListFragment;
import com.example.stage3_project2.Setting.SettingFragment;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private RadioGroup mRgTab;
    private List<Fragment> mFragmentList = new ArrayList<>();
    private String fromWhichFrag;
    private DrawerLayout mDrawerLayout;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Intent intent = new Intent();
        fromWhichFrag = intent.getStringExtra("from frag");

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
                    case R.id.rb_question:
                        changeFragment(QuestionListFragment.class.getName());
                        break;
                    case R.id.rb_setting:
                        changeFragment(SettingFragment.class.getName());
                        break;
                }
            }
        });
        if(savedInstanceState == null){
            if(fromWhichFrag==null){
                changeFragment(HomeFragment.class.getName());
            }
            else if(fromWhichFrag.equals("appointment")){
                changeFragment(AppointmentFragment.class.getName());
            }
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
            } else if (tag.equals(QuestionListFragment.class.getName())) {
                fragment = QuestionListFragment.newInstance();
            } else if (tag.equals(SettingFragment.class.getName())) {
                fragment = SettingFragment.newInstance();
            }
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
