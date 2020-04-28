package com.example.stage3_project2.Bean;

/**
 * <p>描述：写一个用于模拟测试的bean</p>
 * 作者： zhouyou<br>
 * 日期： 2016/10/27 16:25<br>
 * 版本： v2.0<br>
 */
public class TestBean {
    private String title;
    private String content;

    public TestBean(String title, String content) {
        this.title = title;
        this.content = content;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String age) {
        this.content = content;
    }

    @Override
    public String toString() {
        return "TestBean{" +
                "title='" + title + '\'' +
                ", content='" + content + '\'' +
                '}';
    }
}
