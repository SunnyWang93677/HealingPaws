package com.example.stage3_project2.Appointment;

import android.content.Context;
import android.view.View;
import android.widget.Toast;

import com.example.stage3_project2.Bean.MultipleItemBean;
import com.example.stage3_project2.R;

import recyclerview.adapter.HelperRecyclerViewDragAdapter;
import recyclerview.adapter.HelperRecyclerViewHolder;
import recyclerview.swipemenu.SwipeMenuLayout;

public class SwipeMenuAdapter extends HelperRecyclerViewDragAdapter<MultipleItemBean> {
    public SwipeMenuAdapter(Context context) {
        super(context, R.layout.adapter_swipemenu1_layout,R.layout.adapter_swipemenu_layout);
    }

    @Override
    protected void HelperBindData(HelperRecyclerViewHolder viewHolder, int position, MultipleItemBean item) {
        final SwipeMenuLayout superSwipeMenuLayout = (SwipeMenuLayout) viewHolder.itemView;
        superSwipeMenuLayout.setSwipeEnable(true);   //设置是否可以侧滑
        switch (item.getItemType()){
            case 0:
                viewHolder.setText(R.id.title,item.getTitle())//.setImageResource(R.id.image_iv, position)这个也去掉
                        .setOnClickListener(R.id.btStar, new View.OnClickListener() {
                            @Override
                            public void onClick(View view) {
                                Toast.makeText(mContext,"show Favorite",Toast.LENGTH_SHORT).show();
                            }
                        })
                        .setOnClickListener(R.id.btDelete, new View.OnClickListener() {
                            @Override
                            public void onClick(View view) {
                                Toast.makeText(mContext,"show good",Toast.LENGTH_SHORT).show();
                            }
                        });
                viewHolder.setText(R.id.remark, item.getContent());
//                        .setOnClickListener((R.id.image_iv, new View.OnClickListener() {
//                            @Override
//                            public void onClick(View view) {
//                                Toast.makeText(mContext,"show image",Toast.LENGTH_SHORT).show();
//                            }
//                        });
                break;
            case 1:
                viewHolder.setText(R.id.title,item.getTitle()).setOnClickListener(R.id.btStar, new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        Toast.makeText(mContext,"show open",Toast.LENGTH_SHORT).show();
                    }
                }).setOnClickListener(R.id.btDelete, new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        Toast.makeText(mContext,"show delete",Toast.LENGTH_SHORT).show();
                    }
                });//.setImageResource(R.id.image_iv, position);这个暂时去掉
                viewHolder.setText(R.id.remark, item.getContent());

                /**
                 * 设置可以非滑动触发的开启菜单
                 */
//                viewHolder.getView(image_iv).setOnClickListener(new View.OnClickListener() {
//                    @Override
//                    public void onClick(View view) {
//                        if (superSwipeMenuLayout.isOpen()) {
//                            superSwipeMenuLayout.closeMenu();
//                        } else {
//                            superSwipeMenuLayout.openMenu();
//                        }
//                    }
//                });
                break;
        }
    }


    @Override
    public int checkLayout(MultipleItemBean item, int position) {
        return item.getItemType();
    }
}

