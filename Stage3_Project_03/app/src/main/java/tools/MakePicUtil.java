package tools;

import com.example.stage3_project2.R;

import java.util.Random;

/**
 * <p>描述：制造图片工具类</p>
 * 作者： zhouyou<br>
 * 日期： 2018/4/10 14:26 <br>
 * 版本： v1.0<br>
 */
public class MakePicUtil {
    private static int[] pics = {R.drawable.icecream01, R.drawable.icecream02, R.drawable.icecream03
            , R.drawable.icecream04, R.drawable.icecream05, R.drawable.icecream06, R.drawable.icecream07
            , R.drawable.icecream08, R.drawable.icecream01, R.drawable.icecream02, R.drawable.icecream03, R.drawable.icecream04};

    public static int makePic() {
        return pics[new Random().nextInt(pics.length)];
    }
    public static int makePic(int position) {
        return pics[position%pics.length];
    }
}
