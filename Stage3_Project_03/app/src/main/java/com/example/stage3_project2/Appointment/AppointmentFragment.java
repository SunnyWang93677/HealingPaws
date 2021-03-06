package com.example.stage3_project2.Appointment;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.example.stage3_project2.Bean.MultipleItemBean;
import com.example.stage3_project2.R;

import java.util.ArrayList;
import java.util.List;

import recyclerview.adapter.BaseRecyclerViewAdapter;
import recyclerview.swipemenu.SwipeMenuRecyclerView;

public class AppointmentFragment extends Fragment implements SwipeMenuRecyclerView.LoadingListener{

    private SwipeMenuRecyclerView superSwipeMenuRecyclerView;
    private SwipeMenuAdapter swipeMenuAdapter;
    private Button addAppoint;

    public AppointmentFragment() {

    }

    public static AppointmentFragment newInstance() {
        AppointmentFragment fragment = new AppointmentFragment();
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_appointment, container, false);
        superSwipeMenuRecyclerView = view.findViewById(R.id.super_swipemenu_recycle_view);
        LinearLayoutManager layoutManager = new LinearLayoutManager(getActivity());
        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        superSwipeMenuRecyclerView.setLayoutManager(layoutManager);
        superSwipeMenuRecyclerView.setPullRefreshEnabled(true);
        superSwipeMenuRecyclerView.setLoadingMoreEnabled(true);
        superSwipeMenuRecyclerView.setLoadingListener(this);
        superSwipeMenuRecyclerView.setSwipeDirection(SwipeMenuRecyclerView.DIRECTION_LEFT);//左滑（默认）
        addAppoint = (Button)view.findViewById(R.id.addAppointment);
//        initView(view);
        initAdapter(view);
        init();
        return view;
    }

    private void initView(View view){
        superSwipeMenuRecyclerView = view.findViewById(R.id.super_swipemenu_recycle_view);
        LinearLayoutManager layoutManager = new LinearLayoutManager(getActivity());
        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        superSwipeMenuRecyclerView.setLayoutManager(layoutManager);
        superSwipeMenuRecyclerView.setPullRefreshEnabled(true);
        superSwipeMenuRecyclerView.setLoadingMoreEnabled(true);
        superSwipeMenuRecyclerView.setLoadingListener(this);
        superSwipeMenuRecyclerView.setSwipeDirection(SwipeMenuRecyclerView.DIRECTION_LEFT);//左滑（默认）
    }

    private void initAdapter(View view){
        swipeMenuAdapter = new SwipeMenuAdapter(getActivity());
        swipeMenuAdapter.setOnItemClickListener(new BaseRecyclerViewAdapter.OnItemClickListener<MultipleItemBean>() {
            @Override
            public void onItemClick(View view, MultipleItemBean item, int position) {
                Toast.makeText(getActivity(), item.getTitle(), Toast.LENGTH_SHORT).show();
            }
        });

        superSwipeMenuRecyclerView.setAdapter(swipeMenuAdapter);

        List<MultipleItemBean> dataList = new ArrayList<>();
        String[] name = {"Cathy","Bob","Dube","Billy","Thereshod","Cat","Tim","Han"};
        String[] status = {"", "Emergency","", "Emergency","", "Emergency","Emergency", "Emergency","Emergency", "Emergency","", "Emergency"
                ,"", "Emergency","", "Emergency","", "Emergency","Emergency", "Emergency","Emergency", "Emergency"};

        for (int i = 0 ; i < 8 ; i++){
            MultipleItemBean bean;
            if(i==6 || i==7)
                bean = new MultipleItemBean("2020.04.16",name[i],status[i]);
            else if(i<9)
                bean = new MultipleItemBean("2020.04.0"+(i+1),name[i],status[i]);
            else
                bean = new MultipleItemBean("2020.04."+(i+1),name[i],status[i]);
            bean.setItemType(i%2);
            dataList.add(bean);
        }

        swipeMenuAdapter.setListAll(dataList);
    }

    @Override
    public void onRefresh() {
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                superSwipeMenuRecyclerView.refreshComplete();
            }
        },2000);
    }

    @Override
    public void onLoadMore() {
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                superSwipeMenuRecyclerView.loadMoreComplete();
            }
        }, 2000);
    }

    public void init(){
        addAppoint.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), AddAppointment.class);
                intent.putExtra("from Appointment","appointment");
                startActivity(intent);
            }
        });
    }




}
