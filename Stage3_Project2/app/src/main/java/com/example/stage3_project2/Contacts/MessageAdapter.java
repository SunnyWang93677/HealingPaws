package com.example.stage3_project2.Contacts;

import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.example.Reader.R;

import java.util.List;

import androidx.recyclerview.widget.RecyclerView;

public class MessageAdapter extends RecyclerView.Adapter<MessageAdapter.MyViewHolder> {

    private List<Message> mMessageList;

    public MessageAdapter(List<Message> mMessageList) {
        this.mMessageList = mMessageList;
    }

    @Override
    public MyViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = View.inflate(parent.getContext(), R.layout.conversation_item, null);
        MyViewHolder holder = new MyViewHolder(view);
        return holder;
    }

/*
* https://blog.csdn.net/weixin_43980777/article/details/101715641
 */
    @Override
    public void onBindViewHolder(MyViewHolder holder, int position) {
        Message message = mMessageList.get(position);
        if (message.getType() == Message.RECEIVED) {
            holder.LeftFrame.setVisibility(View.VISIBLE);
            holder.RightFrame.setVisibility(View.GONE);
            holder.tv_Left.setText(message.getContent());
        } else if (message.getType() == Message.SEND) {
            holder.LeftFrame.setVisibility(View.GONE);
            holder.RightFrame.setVisibility(View.VISIBLE);
            holder.tv_Right.setText(message.getContent());
        }
    }

    @Override
    public int getItemCount() {

        return mMessageList.size();
    }

    static class MyViewHolder extends RecyclerView.ViewHolder {

        LinearLayout LeftFrame;
        LinearLayout RightFrame;
        TextView tv_Left;
        TextView tv_Right;

        public MyViewHolder(View itemView) {
            super(itemView);
            LeftFrame = (LinearLayout) itemView.findViewById(R.id.ll_msg_left);
            RightFrame = (LinearLayout) itemView.findViewById(R.id.ll_msg_right);
            tv_Left = (TextView) itemView.findViewById(R.id.tv_msg_left);
            tv_Right = (TextView) itemView.findViewById(R.id.tv_msg_right);

        }
    }
}
