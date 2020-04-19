package com.example.stage3_project2.Appointment;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v7.widget.LinearLayoutManager;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.example.stage3_project2.Bean.MultipleItemBean;
import com.example.stage3_project2.R;

import java.util.ArrayList;
import java.util.List;

import recyclerview.adapter.BaseRecyclerViewAdapter;
import recyclerview.swipemenu.SwipeMenuRecyclerView;

public class Emp_AppointWaitTreat extends Fragment implements SwipeMenuRecyclerView.LoadingListener{
    private SwipeMenuRecyclerView superSwipeMenuRecyclerView;
    private SwipeMenuAdapter swipeMenuAdapter;
    private Button emp_appointChange;
    private static boolean flag=true;


    public Emp_AppointWaitTreat() {

    }

    public static Emp_AppointWaitTreat newInstance() {
        Emp_AppointWaitTreat fragment = new Emp_AppointWaitTreat();
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_emp_appoint_part, container, false);
        superSwipeMenuRecyclerView = view.findViewById(R.id.super_swipemenu_recycle_view);
//        emp_appointChange = view.findViewById(R.id.emp_appointChange);


        LinearLayoutManager layoutManager = new LinearLayoutManager(getActivity());
        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        superSwipeMenuRecyclerView.setLayoutManager(layoutManager);
        superSwipeMenuRecyclerView.setPullRefreshEnabled(true);
        superSwipeMenuRecyclerView.setLoadingMoreEnabled(true);
        superSwipeMenuRecyclerView.setLoadingListener(this);
        superSwipeMenuRecyclerView.setSwipeDirection(SwipeMenuRecyclerView.DIRECTION_LEFT);//左滑（默认）
//        addAppoint = (Button)view.findViewById(R.id.addAppointment);
//        initView(view);
        initAdapter(view);
        init();
        return view;
    }



//    private void initView(View view){
//        superSwipeMenuRecyclerView = view.findViewById(R.id.super_swipemenu_recycle_view);
//        LinearLayoutManager layoutManager = new LinearLayoutManager(getActivity());
//        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
//        superSwipeMenuRecyclerView.setLayoutManager(layoutManager);
//        superSwipeMenuRecyclerView.setPullRefreshEnabled(true);
//        superSwipeMenuRecyclerView.setLoadingMoreEnabled(true);
//        superSwipeMenuRecyclerView.setLoadingListener(this);
//        superSwipeMenuRecyclerView.setSwipeDirection(SwipeMenuRecyclerView.DIRECTION_LEFT);//左滑（默认）
//    }

    private void initAdapter(View view){
        swipeMenuAdapter = new SwipeMenuAdapter(getActivity());
        swipeMenuAdapter.setOnItemClickListener(new BaseRecyclerViewAdapter.OnItemClickListener<MultipleItemBean>() {
            @Override
            public void onItemClick(View view, MultipleItemBean item, int position) {
                Toast.makeText(getActivity(), item.getTitle(), Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(getActivity(), Emp_OrderTreat.class);
                startActivity(intent);
            }
        });

        superSwipeMenuRecyclerView.setAdapter(swipeMenuAdapter);

        List<MultipleItemBean> dataList = new ArrayList<>();
        String[] name = {"Cathy","Pop","Han","Steve","Lucy","Lucky","Ken","Oth","Pop","Top","Steve","Lucy","Lucky","Ken","Men","Wang",
                "Ven","Sj","Jin","Chen","Han"};
        String[] status = {"", "Emergency","", "Emergency","", "Emergency","", "Emergency","", "Emergency","", "Emergency"
                ,"", "Emergency","", "Emergency","", "Emergency","Emergency", "Emergency","Emergency", "Emergency"};
        for (int i = 0 ; i < 20 ; i++){
            MultipleItemBean bean;
            if(i<9)
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

    @Override
    public void onResume() {
        super.onResume();
        swipeMenuAdapter.notifyDataSetChanged();
    }

    public void init(){

    }
}
