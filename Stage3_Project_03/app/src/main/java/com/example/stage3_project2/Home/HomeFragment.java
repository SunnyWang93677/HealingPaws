package com.example.stage3_project2.Home;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.support.v4.app.Fragment;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.StaggeredGridLayoutManager;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.Toast;

import com.example.stage3_project2.Bean.TestBean;
import com.example.stage3_project2.Pets.ViewPets;
import com.example.stage3_project2.R;


import java.util.ArrayList;
import java.util.List;

import recyclerview.adapter.BaseRecyclerViewAdapter;
import recyclerview.refresh.ProgressStyle;

public class HomeFragment extends Fragment implements View.OnClickListener{

    private DrawerLayout mDrawerLayout;
    private Button toogleButton;
    private Button pets;

    private recyclerview.XRecyclerView mRecyclerView;
    private StaggeredGridAdapter mAdapter;
    private ArrayList<TestBean> listData;
    private int times = 0;

    String[] mTitles;
    String[] mContents;

    public HomeFragment() {

    }

    public static HomeFragment newInstance() {
        HomeFragment fragment = new HomeFragment();
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_home1, container, false);
        init(view);
        return view;
    }

    private void init(View view){
        mDrawerLayout = view.findViewById(R.id.drawer_layout);
        Toolbar toolbar = (Toolbar) view.findViewById(R.id.toolbar);
        ((AppCompatActivity) getActivity()).setSupportActionBar(toolbar);
        pets = (Button)view.findViewById(R.id.pets);
        pets.setOnClickListener(this);
        toogleButton = (Button) view.findViewById(R.id.toogleButton);
        toogleButton.setOnClickListener(this);
        mTitles = getResources().getStringArray(R.array.titles);
        mContents = getResources().getStringArray(R.array.contents);

        mRecyclerView = (recyclerview.XRecyclerView)view.findViewById(R.id.recyclerview);

        StaggeredGridLayoutManager layoutManager = new StaggeredGridLayoutManager( 2,
                StaggeredGridLayoutManager.VERTICAL);
        layoutManager.setOrientation(LinearLayoutManager.VERTICAL);
        mRecyclerView.setLayoutManager(layoutManager);
        mRecyclerView.setRefreshProgressStyle(ProgressStyle.SysProgress);
        mRecyclerView.setLoadingMoreProgressStyle(ProgressStyle.LineScale);
        mRecyclerView.setArrowImageView(R.mipmap.iconfont_downgrey);

        mRecyclerView.setLoadingListener(new recyclerview.XRecyclerView.LoadingListener() {
            @Override
            public void onRefresh() {
                times = 0;
                new Handler().postDelayed(new Runnable(){
                    @Override
                    public void run() {
                        //不需要先clear  因为用setListAll就是覆盖了
                        //listData.clear();
                        List<TestBean> list = new ArrayList<TestBean>();
                        for(int i = 0; i < 4 ;i++){
                            //listData.add("item" + i + "after " + refreshTime + " times of refresh");
//                            String name =i%2==0?mTitles[0]:mTitles[1];
//                            String age = i%2==0?mContents[0]:mContents[1];
                            String name = mTitles[i];
                            String age = mContents[i];
                            TestBean testBean = new TestBean(name, age);
                            list.add(testBean);
                        }
                        mAdapter.setListAll(list);
//
                        mRecyclerView.refreshComplete();
                    }

                }, 1000);            //refresh data here
            }

            @Override
            public void onLoadMore() {
                if(times < 10){
                    new Handler().postDelayed(new Runnable(){
                        @Override
                        public void run() {
                            mRecyclerView.loadMoreComplete();
                            //改造后的用法
                            List<TestBean> list = new ArrayList<TestBean>();
                            for (int i = 0; i < 10; i++) {
                                String name = (i + listData.size())%2==0?mTitles[0]:mTitles[1];
                                String age = (i + listData.size())%2==0?mContents[0]:mContents[1];
                                TestBean testBean = new TestBean(name, age);
                                list.add(testBean);
                            }

                            //mAdapter.notifyDataSetChanged();
                            //追加list.size()个数据到适配器集合最后面
                            //不需要 mAdapter.notifyDataSetChanged();
                            mAdapter.addItemsToLast(list);

                            mRecyclerView.refreshComplete();
                        }
                    }, 1000);
                } else {
                    new Handler().postDelayed(new Runnable() {
                        @Override
                        public void run() {

                            mAdapter.notifyDataSetChanged();
                            mRecyclerView.loadMoreComplete();
                        }
                    }, 1000);
                }
                times ++;
            }
        });

        listData = new ArrayList<TestBean>();
        for (int i = 0; i < 4; i++) {
//            String name = i%2==0?mTitles[0]:mTitles[1];
//            String age = i%2==0?mContents[0]:mContents[1];
            String name = mTitles[i];
            String age = mContents[i];
            TestBean testBean = new TestBean(name, age);
            listData.add(testBean);
        }

        //方式四对应的初始化适配器   也可采用下面的构造方式创建对象  （自己选择）
        mAdapter = new StaggeredGridAdapter(getActivity());
        /****讲解*****/
        //1.使用setListAll（覆盖数据）后就不需要再调用notifyDataSetChanged（）
        //2.如果是addAll()追加
        //3.自己会刷新
        mAdapter.setListAll(listData);

        //方式一对应的初始化适配器
        //mAdapter = new MyAdapter(listData, this, R.layout.item);
        //方式二对应的初始化适配器
        //mAdapter = new MyAdapter(this, R.layout.item);
        mRecyclerView.setAdapter(mAdapter);

        //设置item事件监听
        mAdapter.setOnItemClickListener(new BaseRecyclerViewAdapter.OnItemClickListener<TestBean>() {
            @Override
            public void onItemClick(View view, TestBean item, int position) {
                Toast.makeText(getContext(),"我是item "+position,Toast.LENGTH_LONG).show();
            }
        });
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.toogleButton:
                mDrawerLayout.openDrawer(GravityCompat.START);
                break;
            case R.id.pets:
                Intent intent = new Intent(getActivity(), ViewPets.class);
                startActivity(intent);

                break;
        }

    }





}
