## 一个语音合成脚本
基于百度开放的语音合成平台, 通过这个脚本, 你可以很方便的将句子按照任意时间格式插入到一个音乐之中.   
你可以用来合成rap等.

## 安装环境
linux下只需要ffmpeg, 一般是默认安装的.  
windows下要下载一个ffmpeg
## 使用方法
#### 准备歌词
在`lylric.txt`中编辑你的歌词
一行对应一个8拍
####  准备乐谱
在`musicbook/musicbook.txt`中编辑你的乐谱, 格式为
```
[time] lyricId_speaker_speed_pitch
```
* time如果为`1`, 则意味着插入到第`1`个4个八拍结束处
* lyricId 和 lylric.txt中歌词的行号匹配既可（lyricId=0 对应 lylric.txt中的第0行歌词）
* speaker 有`1`:机器男生, `2`:机器女生,`3`:感情男生,`4`:感情女生 四个选项
* speed 为0~15的小数
* pitch 为0~9的整数, 数字越大, 音调越高

#### 配置文件
在`config`文件夹下
PERIOD：表示指定音乐一个8拍的时间
DELAY：表示指定音乐前奏时间


#### 生成方式

执行`python gen.py
该代码中，加入了自动协调PERIOD、每行歌词长短与speed的关系
对于一个新的music.mp3只需要在config文件中，添加该music.mp3的配置文件即可

标准配置
PERIOD=1.6 对应speed=6.0
若PERIOD=x 则相应speed=1.6 / x * 6.0

当一行歌词的字数不超过8时，对应speed = s1
当一行歌词的字数超过8时,对应speed = s1 * len(current_line_lyrics) / 8

####
参考：https://github.com/Fancy7777/genRap
