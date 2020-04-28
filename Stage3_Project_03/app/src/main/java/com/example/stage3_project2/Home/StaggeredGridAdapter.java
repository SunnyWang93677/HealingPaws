package com.example.stage3_project2.Home;

import android.content.Context;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;


import com.example.stage3_project2.Bean.TestBean;
import com.example.stage3_project2.R;

import recyclerview.adapter.HelperRecyclerViewHolder;
import tools.MakePicUtil;

/**
 * <p>描述：Staggered适配器</p>
 * 
 * 作者： zhouyou<br>
 * 日期： 2016/10/27 16:24<br>
 * 版本： v2.0<br>
 */
public class StaggeredGridAdapter extends recyclerview.adapter.HelperRecyclerViewAdapter<TestBean> {
    public StaggeredGridAdapter(Context context) {
        super(context, R.layout.item_staggered_grid);
    }

   //不需要自己再自定义viewHolder类了 库里定义有viewHolder基类HelperRecyclerViewHolder
    @Override
    protected void HelperBindData(HelperRecyclerViewHolder viewHolder, int position, TestBean item) {
        //传统的写法是从集合中获取再强转,如下：
        //TestBean testBean =(TestBean)datas.get(position);
        
        //baseadapter中提供的有获取item的方法，直接调用就行了，也不用强转
        final TestBean testBean = getData(position);
        
        //采用链式的设计的书写方式，一点到尾。（方式一）
        viewHolder.setText(R.id.text,testBean.getTitle())
                .setImageResource(R.id.image, MakePicUtil.makePic(position))
        .setOnClickListener(R.id.image, new View.OnClickListener() {//点击事件
            @Override
            public void onClick(View view) {
                Toast.makeText(mContext, "我是子控件" + testBean.getTitle() + "请看我如何处理View点击事件的", Toast.LENGTH_LONG).show();
            }
        });

        //设置某个view是否可见
        //.setVisible(R.id.text,true);
        
        //其它更多连写功能请查看viewHolder类中代码
        
        //通过getView直接获取控件对象，不需要强转了，采用的是泛型（方式二）
        TextView textView =viewHolder.getView(R.id.text2);
        textView.setText(testBean.getContent());
        
        
        //举例  如果想知道适配器中数据是否为空isEmpty()  就可以了  无需list.size()==0  list.isEmpty()等其它方式
        if(isEmpty()){
            
        }
    }

    /*******************注意**********************************/
    //方式一：此方式是另一种处理：绑定相关事件,例如点击长按等,默认空实现，如果你要使用需要覆写setListener()方法
    //方式二：绑定相关事件,例如点击长按等,默认空实现等我们一般会在适配器外部使用，
    // 例如： mAdapter.setOnItemClickListener(new BaseRecyclerViewAdapter.OnItemClickListener<TestBean>(){});
    
    //以上两种item点击事件都可以，自己选择合适的方式
    
   /* @Override
    protected void setListener(HelperRecyclerViewHolder viewHolder, final int position, TestBean item) {
        viewHolder.getItemView().setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Toast.makeText(mContext,"我是Item："+position,Toast.LENGTH_SHORT).show();
            }
        });
    }*/
}
